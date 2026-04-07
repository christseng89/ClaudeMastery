# Batch Service 架构设计

> 国际银行结算平台日终批量服务，支持国内单实体和海外多实体多时区部署。

---

## 一、模块位置与依赖

```
exim-backend/
├── exim-common/         ← 公共模块
├── trade-service/       ← 交易服务 :8080
├── security-service/    ← 安全服务 :8081
├── message-service/     ← 报文服务 :8083
└── batch-service/       ← 日终批量服务 :8084
    ├── 依赖: exim-common
    ├── 调用: trade-service (HTTP，失败告警)
    └── 数据库:
        ├── eximtrx  (业务数据：trx_sod_eod、trx_work_list 等)
        └── eximbatch (批量元数据：batch_execution_log)
```

**技术栈**：Java 17、Spring Boot 3.2、PostgreSQL、Redis（Redisson 分布式锁）、MyBatis

---

## 二、框架核心流程

```
调度器/手动触发
      │
      ▼
 BatchRunner.run()
      │
      ├─ 1. 依赖检查（BatchDependencyChecker）
      │       前置批量是否当日 SUCCESS？
      │
      ├─ 2. 分布式锁（BatchLockService）
      │       Redis tryLock，非阻塞
      │       锁键：batch:lock:{jobName}:{entityId}:{date}
      │
      ├─ 3. 幂等检查（BatchExecutionLogMapper）
      │       RUNNING → 跳过
      │       SUCCESS → 跳过（forceRerun=true 可绕过）
      │
      ├─ 4. 写入 RUNNING 执行记录
      │
      ├─ 5. BatchJob.execute(context)
      │       业务逻辑
      │
      └─ 6. 更新 SUCCESS / FAILED，释放锁
```

跳过状态（SKIPPED / DEPENDENCY_NOT_MET / ALREADY_DONE）不写入数据库，仅返回内存对象。

---

## 三、配置层级

```
application.yml
└── spring.task.scheduling.cron.zone: Asia/Shanghai   ← cron 统一北京时间

application-batch-schedule.yml
├── exim.batch.global-jobs    ← 作业注册表（元数据）
│       dependencies / lock-minutes / description
│       不配 cron，不负责调度
│
└── exim.batch.entities       ← 实体维度调度
        key = entityId（来自 eximuser.sys_busi_unit.c_entity_id）
        每个 job 只需一行 cron，元数据自动继承 global-jobs
```

**继承关系**：entities 下的 job 自动继承 global-jobs 中同名 job 的 `dependencies` 和 `lock-minutes`，只需配置 `cron`。

**互斥规则**：同一 job 在 global-jobs 和 entities 中只能有一处 enabled=true，否则同日触发两次。

---

## 四、多实体支持

不同实体因时区差异，SOD/EOD 触发时间不同。通过 `entities` 块为每个实体单独配置 cron。

```
实体 001（UTC+8）        实体 002（UTC+1）
SYS_EOD: 23:00 北京     SYS_EOD: 18:00 北京
SYS_SOD:  9:00 北京     SYS_SOD:  9:00 北京（北京凌晨 2 点）
```

触发时透传 `entityId`，BatchJob 内部通过 `EntityResolver.resolveUnitCodes(entityId)` 展开该实体下所有机构，逐个处理。

**锁键含 entityId**，不同实体互不阻塞：
```
batch:lock:SYS_EOD:001:2026-04-02
batch:lock:SYS_EOD:002:2026-04-02   ← 独立锁，并行不阻塞
```

---

## 五、核心类说明

| 类 | 职责 |
|---|---|
| `BatchJob` | 所有批量必须实现的接口 |
| `BatchJobContext` | 执行上下文（businessDate / entityId / unitCode / forceRerun / chunkSize） |
| `BatchJobResult` | 执行结果（total / success / skip / message） |
| `BatchRunner` | 执行引擎，统一处理锁、幂等、日志 |
| `BatchScheduler` | 动态 cron 注册（读配置，无需改 Java 即可新增实体） |
| `BatchLockService` | Redis 分布式锁，支持 entityId 维度 |
| `BatchDependencyChecker` | 依赖检查 + 启动时 DAG 环检测 |
| `EntityResolver` | entityId → List\<unitCode\>（查 sys_busi_unit 表） |
| `BatchProperties` | 配置模型（globalJobs / entities） |
| `BatchController` | REST API（列表 / 触发 / 执行记录查询） |

---

## 六、已实现批量

| jobName | 描述 | 依赖 |
|---|---|---|
| `SYS_EOD` | 日终关机，trx_sod_eod c_status: O→C | 无 |
| `SYS_SOD` | 日初开机，d_busi_date+1，c_status: C→O | SYS_EOD |
| `FLOW_ARCHIVE` | 已完结工作流归档（二期）| SYS_EOD |

---

## 七、日终批量依赖链

```
[定时触发]
    │
SYS_EOD              ← 关机
    │
    ▼
FLOW_ARCHIVE         ← 工作流归档（依赖 SYS_EOD）
    │
    ▼
RECONCILIATION       ← 账务对账（未来，依赖 FLOW_ARCHIVE）
    │
[次日定时触发]
    │
SYS_SOD              ← 开机，d_busi_date+1
```

---

## 八、REST API

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/api/batch/jobs` | 列出所有注册批量 |
| POST | `/api/batch/jobs/{jobName}/trigger` | 手动触发批量 |
| GET | `/api/batch/jobs/{jobName}/executions` | 查询执行记录 |
| GET | `/api/batch/health` | 健康检查 |

手动触发请求体（`TriggerRequest`）：
```json
{
  "businessDate": "2026-04-02",
  "entityId": "001",
  "unitCode": null,
  "forceRerun": false,
  "operatorId": "admin"
}
```

---

## 九、关联 trade-service 待完成事项

| 改造点 | 说明 | 优先级 |
|---|---|---|
| `FuncInfoResponse` 增加 `busiDate` | 从 trx_sod_eod 读取真实交易日返回前端 | 高 |
| 提交交易时校验 `c_status` | EOD 后拒绝新交易，提示"系统已日终" | 中 |
| `GET /api/trade/business-date` | 独立查询当前交易日接口 | 中 |
