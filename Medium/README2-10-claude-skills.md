# 2026 年 Claude（及任何编程智能体）必备的 10 项技能

**作者：unicodeveloper | 2026 年 3 月 | 阅读时长：约 20 分钟**

> 本文是关于智能体技能的权威指南，这些技能将从根本上改变 Claude Code、Cursor、Gemini CLI 及其他 AI 编程助手在生产环境中的表现。

---

## 什么是 Claude Code 的智能体技能？

智能体技能是 `SKILL.md` 文件，用于扩展 Claude Code 及其他 AI 编程助手的能力范围。安装某项技能后，你就是在给智能体提供一本专业手册——一套针对特定任务类别的指令、模板和上下文，供其随时调用。技能可以通过斜杠命令（如 `/frontend-design`）显式调用，也可以在智能体识别到相关任务时自动触发。

2025 年底，局面悄然改变。编程智能体不再只是代码补全工具，而是成为了真正的协作伙伴。它们不仅能建议代码，还能构建完整功能、运行测试、查询数据库、生成产物，并发送 Slack 更新。

但一个没有技能加持的原始 Claude、Amp、Cline、Cursor、OpenCode 或 Copilot，就像刚入职的高级工程师：才华横溢，却缺少让他们大展身手所需的项目专属上下文。

截至 2026 年 3 月，Claude Code 技能生态系统已涵盖 Anthropic 官方技能、经过验证的第三方技能，以及数千个兼容通用 `SKILL.md` 格式的社区贡献技能。同一套技能文件适用于 Claude Code、Cursor、Gemini CLI、Codex CLI 和 Antigravity IDE。

---

## 2026 年 Claude Code 必备的 10 项技能

1. **Frontend Design**：生产级 UI 生成
2. **Browser Use**：实时网页与浏览器自动化
3. **Code Reviewer**：自动化代码质量审查与精简
4. **Remotion**：基于 React 的程序化视频创作
5. **Google Workspace (GWS)**：50+ Google API 自动化
6. **Valyu**：网络搜索与实时专业数据访问
7. **Antigravity Awesome Skills**：1,234+ 精选技能库
8. **PlanetScale Database Skills**：模式分支与查询优化
9. **Shannon**：自主 AI 渗透测试
10. **Excalidraw Diagram Generator**：可视化架构图生成

---

## 1. Frontend Design（前端设计）

**问题所在：** 在没有指导的情况下让任何大语言模型构建落地页，结果几乎千篇一律：Inter 字体、白底紫色渐变、极简动画、网格卡片。并无对错之分，只是平淡无奇。

Anthropic 将此称为"分布收敛"。模型在设计决策的统计中心上训练，自然也会复现统计中心的结果。前端设计技能打破了这一模式。

**功能介绍：** 官方 Anthropic frontend-design 技能（截至 2026 年 3 月已有 277,000+ 次安装）会在 Claude 动笔写任何代码之前，先为其提供一套设计体系和设计理念。它能输出大胆的审美选择、独特的排版风格、有意图的配色方案，以及看起来经过精心设计而非随意堆砌的动画效果。

两者之间的差距显而易见：没有技能时，Claude 默认生成安全而平庸的设计；有了技能，输出的组件看起来像经过资深设计师审阅过的作品。

**安装方法：**

```bash
npx skills add anthropics/claude-code --skill frontend-design
```

或直接通过 Claude 的插件页面安装。安装完成后，使用 `/frontend-design` 命令并描述你想构建的内容。

**核心价值：** 这不仅仅是让界面更好看。其真正意义在于让你的产品摆脱用户已经能识别出的"AI 生成"视觉特征。对于注重交付生产级应用的开发者而言，这是第一必装技能。

---

## 2. Browser Use（浏览器操控）

**问题所在：** 编程智能体对实时网页是"盲目"的。它们可以写爬虫，却无法运行；可以描述页面样子，却无法与之交互。如果你的智能体需要填写表单、登录控制台、抓取动态内容，或端到端验证某个已部署的功能是否正常工作，你就会碰壁。Browser Use 技能通过赋予智能体对浏览器的真实控制权来解决这一问题。

**功能介绍：** Browser Use 技能将 Claude 连接到一个无头浏览器实例。智能体可以访问 URL、点击元素、填写表单、提取 JavaScript 渲染页面的内容、截图，并与复杂的 Web UI 进行交互，所有这些都作为自然语言工作流的一部分来完成。

这与爬虫库不同。智能体无需提前了解 DOM 结构，它像人类一样浏览网络：查看、点击、阅读、行动。

**安装方法：**

```bash
npx skills add https://github.com/browser-use/browser-use --skill browser-use
```

**工作流示例：**

> 用户：端到端检查我们预发布环境上的注册流程是否正常，并对任何错误截图。

智能体将：
1. 打开 `https://staging.yourapp.com/signup`
2. 填写测试邮箱和密码
3. 点击"创建账户"
4. 跟随验证邮件链接
5. 对仪表盘截图（确认注册成功）
6. 报告："注册流程正常。发现一个问题：在移动端，'验证邮件'按钮位于首屏以下，见附件截图。"

**核心价值：** Browser Use 将 Claude 从代码生成工具转变为端到端的 QA 工程师、研究分析师和自动化操作员。任何需要人工打开浏览器并点击操作的工作流，现在都可以由智能体处理。这涵盖了开发者日常琐事中相当大的比例。

---

## 3. Code Reviewer（代码审查）

**问题所在：** 智能体写代码很快，而且越来越好。但代码审查能力仍有不足。在默认情况下，大多数编程智能体产出的代码可以通过初读，但往往遗漏更深层的问题：不必要的抽象、重复的逻辑、函数职责过多、命名不一致、缺少边界情况处理。

代码能运行，但未必经得起时间考验。Code Reviewer 技能让质量审查成为第一等步骤，而不是事后补救。

**功能介绍：** code-reviewer 技能会对智能体编写或修改的任何代码执行结构化审查，检查以下内容：

- 可以简化或提取为可复用工具函数的逻辑
- 违反单一职责原则的函数
- 与代码库其余部分不一致的模式
- 性能低效问题（不必要的重渲染、N+1 查询、阻塞操作）
- 无效代码和未使用的导入
- 命名无法传达意图的问题

关键在于，它不只是标记问题，还会修复问题。审查循环在代码呈现给你之前就已完成。

**安装方法：**

```bash
npx claude-code-templates@latest --skill development/code-reviewer
```

Anthropic 也有一个类似功能的官方技能：

```bash
npx skills add anthropics/claude-code --skill simplify
```

**在 `CLAUDE.md` 中配置审查标准：**

```markdown
## 代码审查标准

完成任何实现后，请审查代码中是否存在以下问题：
- 超过 30 行的函数（可能职责过多）
- 重复两次以上的逻辑（提取为工具函数）
- TypeScript 中 `any` 类型的使用（替换为真实类型）
- 超过 3 个 props 且可以合并为对象的组件
- 异步操作缺少错误处理

在向用户呈现代码前运行 /simplify。
```

**审查前后对比示例：**

```typescript
// 审查前
const getUser = async (id: string) => {
  const res = await fetch(`/api/users/${id}`);
  const data = await res.json();
  return data;
};

const getPost = async (id: string) => {
  const res = await fetch(`/api/posts/${id}`);
  const data = await res.json();
  return data;
};

// 审查后：提取通用模式
const fetchResource = async (path: string) => {
  const res = await fetch(path);
  if (!res.ok) throw new Error(`Request failed: ${res.status}`);
  return res.json();
};

const getUser = (id: string) => fetchResource(`/api/users/${id}`);
const getPost = (id: string) => fetchResource(`/api/posts/${id}`);
```

**核心价值：** 代码审查是保持代码库可维护性的关键技能。当智能体不断交付代码而无人审计时，技术债务会迅速积累。一个在你看到输出之前就自动运行的代码审查器，意味着你收到的代码已经是第二稿，而非第一稿。

---

## 4. Remotion（程序化视频）

**问题所在：** 视频能传达文档无法表达的内容。但视频制作需要完全不同的工作流——不同的工具、不同的时间线、不同的团队。大多数开发者在发布功能时不附带视频演示，因为成本太高。Remotion 让这个借口不复存在。

**功能介绍：** Remotion 是一个用 React 程序化创建视频的框架。你不需要时间轴编辑器，只需编写组件；动画就是随时间变化的状态。Claude Code 的 Remotion 智能体技能将自然语言转化为可运行的 Remotion 组件。

工作流：用 prompt 描述你想要的内容，Claude 生成 React/Remotion 代码，你在 Remotion Studio 中预览，然后渲染为 MP4。

**安装方法：**

```bash
npx skills add remotion/agent-skills
```

**在 Claude 中调用：**

```text
/remotion 创建一个 30 秒的产品演示视频，展示我们的 API 仪表盘，包含动画图表和过渡效果
```

**示例输出：**

```jsx
import { AbsoluteFill, useCurrentFrame, interpolate } from "remotion";

export const ApiDemo = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 30], [0, 1]);
  return (
    <AbsoluteFill style={{ backgroundColor: "#0a0a0a", opacity }}>
      <DashboardAnimation frame={frame} />
    </AbsoluteFill>
  );
};
```

**核心价值：** 产品演示、发布公告、说明视频、动态 README 头图——Remotion 技能让任何开发者无需离开代码编辑器就能完成视频制作。

---

## 5. Google Workspace (GWS) 技能

**问题所在：** Google Workspace 拥有 50+ 个 API：Gmail、Drive、Calendar、Docs、Sheets、Slides、Chat、Admin——每个都有自己的客户端库、OAuth 流程和 REST 端点。历史上，构建一个能与 Workspace 交互的智能体意味着需要编写大量集成代码才能起步。

2026 年 3 月，Google 发布了 `gws`，彻底改变了这一局面。

**功能介绍：** `gws` 是一个 CLI 工具，通过 Google 的 Discovery Service 动态发现所有 Google Workspace API，并将其暴露为统一接口。它内置 MCP 服务器，运行一条命令，你的 AI 智能体即可获得完整的 Workspace 访问权限。

数据实力：`gws` 在上线前三天获得了 4,900 个 GitHub 星。

**安装方法：**

```bash
npm install -g @googleworkspace/cli

# 启动带选定 API 的 MCP 服务器
gws mcp -s drive,gmail,calendar,sheets

npx skills add https://github.com/googleworkspace/cli
```

**预置使用场景：**

- **行政助理**：邮件起草、日历管理、会议纪要转 Docs
- **项目经理**：Sheets 任务追踪、Chat 状态更新
- **IT 管理员**：用户管理、权限控制、审计日志
- **销售团队**：CRM 更新、提案生成

**核心价值：** 任何当前需要在 Google 应用之间复制粘贴的工作流，都可以完全自动化。智能体可以读取 Gmail、起草回复、更新 Sheets、创建 Calendar 事件、生成 Docs——所有操作只需一条 prompt。

---

## 6. Valyu：实时网络搜索与专业数据访问

**问题所在：** 编程智能体擅长处理代码，但与现实世界的交互能力较弱——因为现实世界被锁在付费墙、专有数据库和通用搜索无法触达的专业 API 后面。

- 构建金融研究应用？你需要 SEC 文件。
- 构建生物医学工具？你需要 PubMed 和 ChEMBL。
- 构建经济分析仪表盘？你需要 FRED 和 BLS。

没有这些数据源，智能体会生成听起来有道理但实际上过时或虚构的信息。

**功能介绍：** Valyu 技能通过单一 API 将编程智能体连接到 36+ 专业数据源和高质量网络搜索。一次搜索调用即可返回来自全网以及 SEC 10-K 文件、PubMed、ChEMBL（250 万种生物活性化合物）、临床试验、FRED 经济指标、专利数据库和学术出版商的综合结果。

**安装方法：**

```bash
npx skills add https://github.com/valyuai/skills --skill valyu-best-practices
```

**使用示例：**

```python
from valyu import Valyu

client = Valyu(api_key="your-key")

# 定向 SEC 搜索
result = client.search(
    query="半导体公司最新 10-K 文件中披露的风险因素",
    search_type="proprietary",
    included_sources=["valyu/valyu-sec-filings"],
    max_num_results=5
)

# 跨源生物医学搜索
result = client.search(
    query="GLP-1 受体激动剂药物相互作用与临床试验结果",
    search_type="all",
    included_sources=["valyu/valyu-pubmed", "valyu/valyu-chembl", "valyu/valyu-clinical-trials"],
    max_num_results=10
)
```

**性能基准：** 在 FreshQA（600 条时效性查询）上，Valyu 得分 79%，Google 39%，Exa 24%；在金融专项查询上，Valyu 73% vs Google 55%；在 MedAgent（562 条复杂医学查询）上，Valyu 以 48% 领先。

**核心价值：** 能够访问当前权威专有信息的智能体，与那些只能依赖缓存网络数据的智能体，在能力上有本质差距。这正是区分演示 demo 和真正实用工具的关键。

---

## 7. Antigravity Awesome Skills（技能大全）

**问题所在：** 你遇到的每一个智能体技能问题，可能早已有人解决了。但解决方案散落在 GitHub 仓库、博客文章和 Discord 服务器中。你花时间从零写 `SKILL.md` 文件来处理 PR 创建、调试策略、API 设计、安全审计——而经过实战检验的版本早就存在了。

Antigravity Awesome Skills 就是这一问题的精选答案。

**功能介绍：** 这是一个社区维护的技能库，包含 1,234+ 个为各主流 AI 编程助手设计的智能体技能。兼容 Claude Code、Cursor、Gemini CLI、Codex CLI、GitHub Copilot、Antigravity IDE 等。所有技能遵循通用 `SKILL.md` 格式，按类别组织，一条命令即可安装。

**22,000+ GitHub 星，3,800+ Fork，截至 2026 年 3 月更新至 v7.3.0。** 这是目前最全面的技能集合。

**安装方法：**

```bash
# Claude Code
npx antigravity-awesome-skills --claude

# 其他工具
npx antigravity-awesome-skills --cursor      # Cursor
npx antigravity-awesome-skills --gemini      # Gemini CLI
npx antigravity-awesome-skills --antigravity # Antigravity IDE
npx antigravity-awesome-skills --path ./my-skills # 自定义路径
```

**必知入门技能：**

- `@brainstorming`：写代码前的结构化规划
- `@architecture`：系统设计与组件结构
- `@debugging-strategies`：系统化排查故障手册
- `@api-design-principles`：API 形态、一致性、版本控制
- `@security-auditor`：安全导向的代码审查
- `@lint-and-validate`：轻量级质量检查
- `@create-pr`：将工作打包成简洁的 Pull Request
- `@doc-coauthoring`：结构化技术文档

**角色捆绑包：**

- **Web 向导**：frontend-design、api-design-principles、lint-and-validate、create-pr
- **安全工程师**：security-auditor、lint-and-validate、debugging-strategies
- **核心必备**：brainstorming、architecture、debugging-strategies、doc-coauthoring、create-pr

**核心价值：** 这是让"我应该为此写个技能"待办事项永远清零的技能库。1,234 个技能覆盖了大多数开发者甚至还没想到要自动化的领域——从 AWS CloudFormation 模式到结构化产品思维，再到多语言文档。

---

## 8. PlanetScale Database Skills（数据库技能）

**问题所在：** 数据库工作是智能体最容易犯错的地方。六个月后才会造成痛苦的 Schema 设计决策；在 100 行时正常、100,000 行时崩溃的查询；只在生产环境才发现的缺失索引。

智能体往往把数据库当作普通代码来对待——写出能运行的东西就结束了。

**功能介绍：** PlanetScale 数据库技能教会智能体：

- 使用 PlanetScale 的外键和分支约定设计 Schema
- 正确使用索引编写查询（并标记无法使用索引的情况）
- 使用 `pscale` CLI 创建分支、部署请求和管理迁移
- 将 Schema 变更视为代码——可审查、可回滚

**安装方法：**

```bash
# 安装 pscale CLI
brew install planetscale/tap/pscale

# 登录
pscale auth login

# 安装技能
npx skills add planetscale/agent-skill
```

**端到端工作流示例：**

> 用户：在 Schema 中添加用户偏好设置

智能体将：

1. 创建新数据库分支：`pscale branch create mydb add-user-prefs`
2. 切换到该分支的连接
3. 设计 Schema（含正确索引）
4. 验证索引是否覆盖预期的查询模式
5. 创建部署请求：`pscale deploy-request create mydb add-user-prefs`
6. 报告："Schema 已准备好审查。部署请求 #14 已创建。注意：user_id 没有外键约束，遵循 PlanetScale 水平扩展约定。"

**有无技能的查询对比：**

```sql
-- 没有技能时
SELECT * FROM orders WHERE status = 'pending' AND created_at > '2026-01-01';

-- 有 PlanetScale 技能时
SELECT id, user_id, total, created_at
FROM orders
WHERE status = 'pending'
  AND created_at > '2026-01-01';
-- 新增复合索引：INDEX idx_status_created (status, created_at)
-- 避免 SELECT *，只获取所需列
-- 1000 万行时的查询时间估算：有索引 ~2ms vs 无索引 ~8s
```

**核心价值：** 第一天做出的数据库决策，是第 365 天最难撤销的。一个具备 PlanetScale 技能的智能体，不只是写出能运行的 Schema，而是写出能扩展的 Schema——并且将分支工作流内嵌其中，使每次变更都可审查。

---

## 9. Shannon：自主 AI 渗透测试

**问题所在：** 安全测试是大多数开发团队跳过的步骤——不是因为不在乎，而是因为它昂贵、缓慢，且需要专业知识。传统渗透测试花费数千美元，两周后返回一份 PDF 报告。与此同时，代码库还在不断演进。

Shannon 是一个自主渗透测试智能体，针对你的本地或预发布环境运行，执行真实漏洞利用，并且只报告它能实际证明的漏洞。

**功能介绍：** Shannon 技能封装了 KeygraphHQ 的 Shannon——一个白盒安全测试框架，分析源代码、绘制攻击面，并在 OWASP 5 大类别的 50+ 漏洞类型上执行真实攻击。

**值得关注的基准数据：** 在 XBOW 安全基准（100/104 个漏洞利用）上达到 96.15% 的漏洞利用成功率。这不是标记潜在问题的扫描器，而是一个要么实际利用漏洞、要么不报告的智能体。

**安装方法：**

```bash
npx skills add unicodeveloper/shannon
```

前提条件：Docker 和 Anthropic API 密钥，仅此而已。

**运行方式：**

```bash
# 对本地应用执行完整渗透测试
/shannon http://localhost:3000 myapp

# 针对特定漏洞类别
/shannon --scope=xss,injection http://localhost:8080 frontend

# 命名工作区（支持中断后恢复）
/shannon --workspace=audit-q1 http://staging.example.com backend-api

# 查看运行中的渗透测试状态
/shannon status

# 查看最新报告
/shannon results
```

**五阶段流水线（尽可能并行运行）：**

1. **预侦察**：静态源代码分析 + 外部扫描（Nmap、Subfinder、WhatWeb）
2. **侦察**：通过无头浏览器进行实时攻击面测绘
3. **漏洞分析**：5 个并行智能体（注入 / XSS / SSRF / 认证 / 授权）
4. **漏洞利用**：并行执行，每个智能体生成专用利用智能体
5. **报告**：管理层摘要 + 每个发现的可复现 PoC

**涵盖的 50+ 漏洞类型：**

- **注入**：SQL 注入（联合、盲注、时间盲注）、命令注入、SSTI、NoSQL 注入
- **XSS**：反射型、存储型、DOM 型、文件上传型、Mutation XSS
- **SSRF**：内网服务访问、云元数据（AWS/GCP/Azure）、DNS 重绑定、协议走私
- **认证失效**：默认凭据、JWT 缺陷（none 算法、弱签名）、会话固定、CSRF、MFA 绕过
- **授权失效**：IDOR、权限提升、路径遍历、强制浏览、批量赋值

**成本与时间：** 每次完整渗透测试约 1–1.5 小时，使用 Claude Sonnet 约 $50。

**内置安全门：** Shannon 在每次运行前确认授权，警告不要对生产目标使用，支持范围控制和回避规则，并在 Docker 内运行所有攻击工具——不在宿主机上执行任何操作。

> ⚠️ **重要提示：Shannon 执行真实攻击。请仅在你拥有或拥有明确书面授权的系统上运行。该技能在每次调用时都强制执行授权门控。**

**核心价值：** 大多数代码库存在安全漏洞，而这些漏洞在代码审查中得以幸存，原因是审查者在阅读功能代码时并不会从对抗性角度思考。Shannon 就是那个对抗性检查——自动针对每次预发布部署运行，找出你上周二发布的 API 端点中的 IDOR 漏洞，证明那个所有人都以为已参数化的搜索框中的 SQL 注入。

"无利用，不报告"的原则意味着零误报噪音。你只需修复经过确认的破损之处。

---

## 10. Excalidraw Diagram Generator（可视化架构图生成）

**问题所在：** 架构决策、系统设计、数据流说明——这些都被记录在散文或白板会议中，而没有人记录那些会议。代码注释描述某样东西是什么，图表展示它为何如此结构化。

大多数智能体可以用文字描述一个架构，但几乎没有能生成能够在视觉上说明问题的图表的。Excalidraw 图表生成技能改变了这一点。

**功能介绍：** 该技能从自然语言描述生成生产级 Excalidraw 图表。其设计理念独特之处在于：

- **图表用于论证，而非展示**：每个形状和分组都映射它所代表的概念——一对多关系用扇出结构，顺序流程用时间轴布局，聚合用收敛形状
- **证据产物**：技术图表内联包含实际代码片段和真实 JSON 载荷，而非占位符文本
- **视觉自我验证**：技能包含基于 Playwright 的渲染流水线——智能体生成 Excalidraw JSON，渲染为 PNG，审查自己的输出是否有布局问题（文字重叠、箭头错位、间距不均），并在呈现结果前修复问题

**安装方法：**

```bash
npx skills add https://github.com/coleam00/excalidraw-diagram-skill --skill excalidraw-diagram
```

**示例 prompt：**

```text
创建一个 Excalidraw 图表，展示请求如何流经我们的 API 网关、
认证中间件和下游服务

为多租户 SaaS 生成架构图，包含每个租户独立的数据库 Schema
和共享分析层

绘制 OAuth2 PKCE 流程的时序图，包含浏览器、授权服务器和资源服务器
```

**品牌定制：** 所有颜色存放在 `references/color-palette.md` 中，修改一次，所有图表自动遵循你的配色方案。

**核心价值：** 图表是比产生它们的对话存续时间更长的产物。仓库中一张好的架构图能向六个月后加入的工程师传达设计决策，向不会读代码的利益相关者解释系统，并迫使设计者思考散文描述所掩盖的边界情况。

自我验证循环让这一切真正可用：你得到的是一张可以直接发布的图表，而不是一份会让你感到难为情的草稿。

---

## 如何在 2026 年思考智能体技能

技能是你对智能体能力的投资。原始智能体是通用的，有技能加持的智能体是专业化的。上述 10 项技能覆盖了智能体在没有指导时表现欠佳的约 80% 的工作流：

| 技能 | 解决问题 |
|------|---------|
| Frontend Design | 设计质量 |
| Browser Use | 实时网页访问 |
| Code Reviewer | 代码质量 |
| Remotion | 视频内容创作 |
| Google Workspace | 工作区自动化 |
| Valyu | 网络搜索与专有数据访问 |
| Antigravity Awesome Skills | 技能库（1,234+ 个，一键安装） |
| PlanetScale | 数据库架构 |
| Shannon | 安全验证（96.15% 漏洞利用成功率，零误报） |
| Excalidraw | 可视化沟通 |

评估任何技能时的关键问题：**它是否改变了默认行为，还是只添加了一个你要记住去调用的命令？**

最好的技能在无需持续提示的情况下改变智能体的输出。

- `frontend-design` 改变了"帮我构建落地页"的返回结果
- `Shannon` 在任何内容进入生产前执行对抗性检查
- `Excalidraw` 技能生成你实际可以分享的图表，而不是你自己会重新绘制的占位图

这就是标准。达到这个标准的技能值得花十分钟配置。

---

## 统一安装方式

```bash
# Anthropic 官方技能
npx skills add anthropics/claude-code --skill <skill-name>

# Antigravity Awesome Skills（一次安装 1,234+ 个）
npx antigravity-awesome-skills --claude

# Shannon 自主渗透测试
npx skills add unicodeveloper/shannon

# Excalidraw 图表生成
npx skills add https://github.com/coleam00/excalidraw-diagram-skill --skill excalidraw-diagram

# 列出已安装技能
npx skills list
```

智能体技能生态系统正在快速发展。你还可以每天访问 [https://www.aitmpl.com/skills](https://www.aitmpl.com/skills) 和 [skills.sh](https://skills.sh) 获取最新技能资源，持续扩充你的工具库。

---

## 常见问题解答

**Q：什么是 Claude Code 技能？**

Claude Code 技能是一个 `SKILL.md` 文件，为智能体提供针对特定任务的专业指令、上下文和工作流。技能可通过斜杠命令（如 `/frontend-design`）调用，或根据任务自动触发。同一 `SKILL.md` 格式适用于 Claude Code、Cursor、Gemini CLI 等兼容智能体。

**Q：如何在 Claude Code 中安装技能？**

大多数技能通过 `npx skills add <org>/<repo>` 安装。官方 Anthropic 技能使用 `npx skills add anthropics/claude-code --skill <name>`。Antigravity Awesome Skills 库通过 `npx antigravity-awesome-skills --claude` 一次安装 1,234+ 个技能。使用 `npx skills list` 查看已安装技能。

**Q：提升前端代码质量的最佳技能是什么？**

视觉设计质量：安装官方 Anthropic frontend-design 技能（`npx skills add anthropics/claude-code --skill frontend-design`，277K+ 安装量）。代码质量与精简：安装 simplify 技能（`npx skills add anthropics/claude-code --skill simplify`）。

**Q：Valyu 技能是做什么的？**

Valyu 技能将 Claude Code 连接到网络搜索和 36+ 专业数据源，包括 SEC 文件、PubMed、ChEMBL、ClinicalTrials.gov、FRED 经济指标和学术出版商。安装命令：`npx skills add valyuAI/skills`。Valyu 在 FreshQA 基准上得分 79%，而 Google 仅为 39%。

**Q：Shannon 是做什么的？**

Shannon 是一个自主 AI 渗透测试技能，对 Web 应用执行真实安全漏洞利用。在 XBOW 基准上达到 96.15% 的漏洞利用成功率，涵盖 OWASP 5 大类别的 50+ 漏洞类型。完全在 Docker 中运行，每次完整渗透测试约需 $50。安装命令：`npx skills add unicodeveloper/shannon`。**仅在你拥有授权的系统上使用。**

**Q：什么是 Antigravity Awesome Skills？

Antigravity Awesome Skills 是一个社区维护的技能库，包含 1,234+ 个兼容 Claude Code、Cursor、Gemini CLI 等 7 款以上 AI 编程工具的智能体技能。目前拥有 22,034 个 GitHub 星，安装命令为 `npx antigravity-awesome-skills --claude`。涵盖头脑风暴、架构设计、调试、API 设计、安全审计、PR 创建和文档撰写等各类技能。

**Q：Excalidraw 图表技能是如何工作的？**

Excalidraw 图表技能将自然语言转化为 Excalidraw JSON，使用 Playwright 渲染为 PNG，审查图片是否存在布局问题，修复后再交付一个干净的图表文件。其设计理念是让视觉结构映射概念结构，而非默认使用千篇一律的卡片网格。

**Q：哪些技能同时支持 Claude Code 和 Cursor？**

采用通用 `SKILL.md` 格式的技能两者均支持。Antigravity Awesome Skills 库（`npx antigravity-awesome-skills`）是最大的跨平台兼容集合。Google Workspace（`gws`）和 PlanetScale 技能也支持多种智能体。Remotion、Shannon、Valyu 和 Excalidraw 技能主要面向 Claude Code，但同样遵循可移植格式。

---

## 总结：10 项技能及使用时机

- **Frontend Design**：只要你在构建任何面向用户的 UI，并希望生成的代码不带 AI 通用(**大多数人都用**)痕迹，就应安装。
- **Browser Use**：只要你的智能体需要与实时网页交互、运行端到端测试或研究动态内容，就应安装。
- **Code Reviewer（Simplify）**：每个项目都应安装。自动将智能体代码的第一稿(**自动**跑一遍审查、发现问题、修好，再交给你)转化为第二稿。
- **Remotion**：需要在无独立视频制作流程的情况下制作视频内容（演示、发布、说明视频），就应安装。
- **Google Workspace（GWS）**：团队使用 Google Workspace，并希望智能体能读写 Gmail、Drive、Sheets 和 Calendar，就应安装。
- **Valyu**：应用需要当前权威的专有数据——SEC 文件、研究论文、临床数据、经济指标，就应安装。
- **Antigravity Awesome Skills**：每台机器都应安装。1,234+ 个技能，一条命令，覆盖几乎所有工程工作流。
- **PlanetScale Database Skills**：基于 PlanetScale 或 MySQL 兼容 / Postgres 基础设施构建，并希望默认具备索引感知的 Schema 生成能力，就应安装。
- **Shannon**：在开发和预发布环境中将部署前安全验证列为优先项，就应安装。**切勿在生产环境或无授权系统上运行。**
- **Excalidraw Diagram Generator**：架构决策需要以可视化方式记录，并希望图表作为开发工作流的一部分自动生成，就应安装。
