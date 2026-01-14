以下為中文翻譯：

---

# MCP Server（模型上下文协议服务器）

## 支持顺序思考（Sequential Thinking）的 MCP Server

[https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking](https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking)

### 概述（Overview）

Sequential Thinking MCP Server 提供一种**结构化、逐步推进的思考流程**，用于动态且具反思能力的问题解决。
它可以将复杂问题拆解为可管理的步骤，并支持在分析过程中进行修正与探索替代推理路径。

### 功能特性（Features）

* ✅ 将复杂问题**拆解为可管理的步骤**
* ✅ 随着理解加深，**修正与细化思路**
* ✅ 支持**分支到不同的推理路径**
* ✅ 通过索引跟踪思考过程（`thoughtNumber`, `totalThoughts`）
* ✅ 分析过程中可**动态调整总思考步骤数**
* ✅ **迭代生成并验证**解决方案假设
* ✅ 在多步推理过程中**保持上下文连续性**

### 工具：`sequential_thinking`

该服务器提供一个名为 `sequential_thinking` 的工具，用于支持详细的逐步思考过程。

**参数说明：**

* `thought` (string) —— 当前思考步骤的内容
* `nextThoughtNeeded` (boolean) —— 是否还需要下一步思考
* `thoughtNumber` (integer) —— 当前思考步骤的编号
* `totalThoughts` (integer) —— 当前预计的总思考步骤数
* `isRevision` (boolean，可选) —— 标记该步骤为修正内容
* `revisesThought` (integer，可选) —— 指定正在修正的思考编号
* `branchFromThought` (integer，可选) —— 指定从哪一步开始分支
* `branchId` (string，可选) —— 分支推理路径的标识符

### 常见使用场景（Common Use Cases）

* 🧩 **复杂问题拆解** —— 将架构决策拆分为多个步骤
* 🔁 **带纠偏的规划** —— 对策略进行迭代式修正
* 🌿 **探索性推理** —— 并行测试多种解决思路
* 🐞 **调试与根因分析** —— 系统化定位问题原因
* 📐 **算法设计** —— 逐步构建并验证逻辑

### 安装方式（Installation）

```bash
claude
claude mcp add sequential-thinking --scope project -- npx -y @modelcontextprotocol/server-sequential-thinking

quit

claude
/mcp

   sequential-thinking · ◯ connecting…. 卡住时修复方式如下

quit
claude
/mcp

   sequential-thinking · ✔ connected

/clear
/auto-commit 

请重构 memory-hands-on/src/api 目录下的代码以添加 models。请使用 MCP server 与 sequential_thinking。
```

### 配置（Configuration）

**可选环境变量：**

* `DISABLE_THOUGHT_LOGGING=true` —— 禁用思考过程日志记录

### 示例用法（Example Usage）

安装并重启后，可使用 `sequential_thinking` 工具：

```python
# 示例 1：初步问题拆解
sequential_thinking({
    "thought": "需要优化费用追踪 API 的数据库查询",
    "thoughtNumber": 1,
    "totalThoughts": 5,
    "nextThoughtNeeded": True
})

# 示例 2：修正之前的思考
sequential_thinking({
    "thought": "实际上，对 user_id 和 date 字段建立索引会最有效",
    "thoughtNumber": 3,
    "totalThoughts": 5,
    "isRevision": True,
    "revisesThought": 2,
    "nextThoughtNeeded": True
})

# 示例 3：探索替代方案
sequential_thinking({
    "thought": "替代方案：使用查询结果缓存，而不是数据库优化",
    "thoughtNumber": 4,
    "totalThoughts": 6,
    "branchFromThought": 2,
    "branchId": "caching-approach",
    "nextThoughtNeeded": True
})
```

### 优势（Benefits）

* 🧠 将 AI 推理结构化为**清晰、可追踪的步骤**
* 🔄 支持在不丢失上下文的情况下进行**迭代式改进**
* 🌱 可并行探索多条解决路径
* 🚀 显著提升复杂问题的解决能力
* 🧾 使 AI 的思考过程**可审计、可回溯**

---
