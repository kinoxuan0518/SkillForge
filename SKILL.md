---
name: skillforge
description: >
  AI skill generator powered by NotebookLM MCP + Claude pipeline. Creates reusable SKILL.md files
  following skill-creator standards (lean structure, progressive disclosure, proper degrees of freedom).
  Uses NotebookLM as external knowledge sink for best practices, plus user interviews for org-specific
  constraints. Supports auto mode (requires notebooklm-mcp) and manual mode. Triggers: "make a skill",
  "create a skill for X", "turn X into reusable method", "沉淀成SKILL.md", "把X做成可复用方法".
---

# SkillForge

> AI Skill Generator powered by NotebookLM MCP + Claude

---

## Step 0 — Environment Check (First-time Setup)

### Mode Selection

| Mode | Requirement | Experience |
|------|-------------|------------|
| **Auto Mode** | notebooklm-mcp installed | AI handles everything, user just answers questions |
| **Manual Mode** | No MCP needed | User operates NotebookLM manually, copies output to AI |

### Before You Start

```
Do you have notebooklm-mcp installed?

A) ✅ Yes → Use Auto Mode
B) ❌ No, use Manual Mode → I'll provide NotebookLM search commands
C) 🔧 No, but I want to install → Follow the steps below
```

### Installing NotebookLM MCP (Option C)

**1. Install**
```bash
# Mac/Linux (requires sudo)
sudo npm install -g notebooklm-mcp

# Or use npx (no installation needed)
npx notebooklm-mcp
```

**2. Configure Your AI Tool**

| Tool | Command |
|------|---------|
| **Claude Code** | `claude mcp add notebooklm-mcp notebooklm-mcp` |
| **Opencode** | `opencode mcp add` → name: `notebooklm` / type: `Local` / command: `notebooklm-mcp` |
| **Cursor** | Edit `~/.cursor/mcp.json` |

**Cursor/Other Tools Config:**
```json
{
  "mcpServers": {
    "notebooklm": {
      "command": "notebooklm-mcp"
    }
  }
}
```

**3. Authenticate Google Account**

In your AI tool, say:
```
Please use setup_auth tool to login to Google
```

**4. Verify Installation**
```
Please list my NotebookLM notebooks
```

Once installed, proceed to Step 1.

---

前提：以 `skill-creator` 作为规范底座，不改变其核心约束：
- Frontmatter 仅 `name` + `description`
- SKILL.md 精简（<500行），只写执行必需的流程/护栏
- 细节下沉到 `references/`，确定性动作下沉到 `scripts/`
- 不引入无用文件（README/INSTALL/CHANGELOG 等）

目标：把 Skill 做成三层：
1) **External Canon（外部最佳实践）**：NotebookLM notebook（不打包进 skill）
2) **Local Overlay（本地化约束）**：`references/user_overrides.md`
3) **Execution OS（执行系统）**：`SKILL.md`（薄、硬、可触发、可导航）

---

## 0. 快速判定：这是 Skill 吗
- 是否在教 “how-to（可迁移的做法）” 而不是 “do-now（单次任务指令）”？
- 是否能迁移到 ≥3 个相似场景？
不满足则不做 Skill。

---

# 端到端流程（6步）

## Step 1 — 范围卡（先锁边界）
产出范围卡（草稿，不打包）：
- 一句话目标（可验收）
- 触发语句（5条）
- ✅必须覆盖（3）/ ❌不覆盖（3）
- 输出形态（模板/脚本/决策树/排障表）
- 成功标准（可测）

规则：目标>1 或覆盖场景>5 → 拆子技能。

## Step 2 — 决定自由度与资源形态（决定写法）
- 高自由度：多解、依赖语境 → SKILL.md 给判断框架 + 示例
- 中自由度：有推荐套路可配置 → 伪代码/参数化脚本 + references
- 低自由度：脆弱易错需一致 → `scripts/` 固化步骤 + 少参数

## Step 3 — External Canon：NotebookLM 作为外部知识沉淀
NotebookLM 负责：收集来源、聚合阅读、结构化提取（最佳实践层）。
来源要求（3–8条，强制配比）：
- 1 权威/官方/标准
- 1 可复现案例（步骤/数据）
- 1 踩坑/反例（症状-原因-修复）
淘汰：无作者/无日期/纯观点/无可验证细节。

（若有 MCP）建议：自动建 notebook + add_source；否则手动导入。

## Step 4 — 提取契约（NotebookLM 输出必须“可编译”）
对 NotebookLM 的提问要求：
- 只输出可执行 know-how（步骤/规则/模板/边界/排障）
- 每条关键结论带“来源要点”（一句话即可，避免只贴URL）
- 无法确认标 `UNVERIFIED`

强制输出结构：
- Quickstart（3步）
- Decision points（if/else）
- Templates（≥2）
- Failure modes（≥5，含修复动作）
- Edge cases（≥3）

## Step 5 — Local Overlay：短问诊，获得用户/组织真实约束
目的：避免“正确但不适用”。只问会改变动作选择的问题（不要长访谈）。

最小问诊模板（建议一次问完）：
1) 组织红线/合规限制是什么？（绝对不能做的事）
2) 必须使用的工具/平台是什么？（以及不能用的）
3) 产物格式固定吗？（字段/模板/命名/交付渠道）
4) 你更优先：速度/准确/可解释/一致性？（选1）
5) 历史最常翻车的3个点？（症状即可）

把答案写入：`references/user_overrides.md`（可以较详细）。

## Step 6 — 编译为 Skill（把 A+B 编译成“执行系统”）
编译规则：
- 外部知识（Canon）提供默认路径与上限；本地约束（Overlay）钉死边界与口径。
- 冲突裁决：
  1) 合规/组织硬约束 > 2) 用户偏好 > 3) 外部最佳实践
- 把“分歧点”显式写入 SKILL.md：
  - Default（外部最佳实践）
  - Override（组织/用户要求）
  - Trade-off（代价/风险）

内容去向（必须遵守）：
- SKILL.md：最短路径、决策点、护栏、排障、导航
- references/：Schema/变体/长示例/组织口径（含 user_overrides）
- scripts/：确定性动作（低自由度）
- NotebookLM：外部资料原文与更新频繁信息（不进包）

---

# 质量闸门（轻量 DoD）
发布前必须满足：
- description 写清触发条件与适用范围（触发语/不适用）
- Quickstart 30秒可开始做
- ≥2 可复制模板/命令/示例
- ≥5 Failure modes（含修复）
- ≥3 Edge cases
- 脆弱任务：脚本化或严格参数约束
- SKILL.md < 500行；否则拆分

---

# SKILL.md 推荐最小骨架（薄、硬、可导航）

## Quickstart（3步）
1) …
2) …
3) …

## Workflow（含决策点）
- If … → …
- Else … → …

## Guardrails（自由度护栏）
- 允许变动：…
- 不允许变动：…
- 必须确认：…

## Templates / Commands（≥2）
- …

## Failure modes（≥5）
- 症状：… → 修复：…

## Edge cases（≥3）
- …

## References navigation（按需加载）
- 用户/组织覆盖层：`references/user_overrides.md`
- Schema/变体：`references/<topic>.md`
- 示例集合：`references/examples.md`

---

# 资源文件建议（仅当需要）
- `references/user_overrides.md`：本地化约束（必需）
- `references/schema.md`：数据结构/API（按需）
- `references/<variant>.md`：多平台/多框架变体（按需）
- `scripts/*.py|.sh`：确定性执行脚本（按需）
- `assets/`：输出模板/品牌素材（按需）
