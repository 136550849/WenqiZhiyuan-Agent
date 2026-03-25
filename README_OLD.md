# TradingAgents-CN + OpenClaw 配置指南

> 配置日期：2026-03-17
> 版本：v2.0

---

## 📋 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    TradingAgents-CN 平台                      │
│              http://localhost:9981/workflow/agents           │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ API 集成
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    OpenClaw Gateway                          │
│                   Port: 18789                                │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ Agent 路由
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   13 个交易 Agent                              │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│  │ 市场分析师   │ │ 基本面分析师 │ │ 技术分析师   │        │
│  │ 📊          │ │ 💰          │ │ 📈          │        │
│  └──────────────┘ └──────────────┘ └──────────────┘        │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│  │ 新闻分析师   │ │ 风险分析师   │ │ 交易经理     │        │
│  │ 📰          │ │ ⚠️          │ │ 🎯          │        │
│  └──────────────┘ └──────────────┘ └──────────────┘        │
│  ... (共 13 个)                                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ 数据调用
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Tushare 数据接口                            │
│              API: api.tushare.pro                            │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Agent 目录结构

```
G:\trading-agents\
├── market-analyst\          # 市场分析师 📊
│   ├── SOUL.md             # 人格定义
│   ├── AGENTS.md           # 行为准则
│   ├── MEMORY.md           # 长期记忆
│   └── memory\             # 每日笔记
│
├── fundamental-analyst\     # 基本面分析师 💰
│   └── SOUL.md
│
├── technical-analyst\       # 技术分析师 📈
│   └── SOUL.md
│
├── news-analyst\            # 新闻分析师 📰
│   └── SOUL.md
│
├── sentiment-analyst\       # 情绪分析师 😊
│   └── SOUL.md
│
├── risk-analyst\            # 风险分析师 ⚠️
│   └── SOUL.md
│
├── portfolio-manager\       # 组合经理 💼
│   └── SOUL.md
│
├── trading-manager\         # 交易经理 🎯
│   └── SOUL.md
│
├── research-lead\           # 研究主管 🔬
│   └── SOUL.md
│
├── researcher-1\            # 行业研究员 🏭
│   └── SOUL.md
│
├── researcher-2\            # 公司研究员 🏢
│   └── SOUL.md
│
├── trader\                  # 交易员 💹
│   └── SOUL.md
│
└── post-processor\          # 报告生成 📄
    └── SOUL.md
```

---

## ⚙️ OpenClaw 配置

### 配置文件位置
`C:\Users\汇语读书\.openclaw\openclaw.json`

### Agent 配置片段
```json
{
  "agents": {
    "list": [
      {
        "id": "market-analyst",
        "name": "市场分析师",
        "workspace": "G:\\trading-agents\\market-analyst",
        "agentDir": "C:\\Users\\汇语读书\\.openclaw\\agents\\market-analyst\\agent",
        "model": "qwen/qwen3.5-plus",
        "identity": {
          "name": "市场分析师",
          "emoji": "📊"
        }
      },
      // ... 其他 12 个 agent
    ]
  }
}
```

---

## 🔑 Tushare 配置

### 获取 Token
1. 访问 https://tushare.pro
2. 注册账号
3. 在个人中心获取 Token

### 配置 Token
```powershell
# PowerShell - 设置环境变量
[Environment]::SetEnvironmentVariable("TUSHARE_TOKEN", "你的 token", "User")
```

### 验证配置
```python
import tushare as ts
import os

token = os.environ.get("TUSHARE_TOKEN")
pro = ts.pro_api(token)

# 测试调用
df = pro.daily(ts_code='000001.SZ', start_date='20260317', end_date='20260317')
print(df)
```

---

## 🚀 使用指南

### 方式 1：通过 TradingAgents-CN 平台

1. 访问 http://localhost:9981/workflow/agents
2. 选择要查看的 Agent
3. 点击"查看详情"查看配置
4. 点击"调试"测试提示词

### 方式 2：通过 OpenClaw 命令行

```bash
# 查看所有 agent
openclaw agents list

# 查看特定 agent 配置
openclaw agents list --json | jq '.[] | select(.id=="market-analyst")'

# 测试 agent
openclaw sessions spawn --agent market-analyst --task "分析 000001.SZ 的技术面"
```

### 方式 3：通过 Control UI

```bash
# 打开控制面板
openclaw dashboard
```

在浏览器中访问 http://localhost:18789

---

## 📊 Agent 协作流程

### 单股分析流程

```
1. 用户请求：分析 000001.SZ
         │
         ▼
2. trading-manager 接收任务
         │
    ┌────┴────┬────────────┬────────────┐
    ▼         ▼            ▼            ▼
3. market   fundamental  news       risk
   analyst   analyst     analyst    analyst
    │         │            │            │
    └─────────┴────────────┴────────────┘
              │
              ▼
4. trading-manager 整合各方观点
              │
              ▼
5. trader 生成交易计划
              │
              ▼
6. post-processor 生成最终报告
```

---

## 🧠 Agent 成长机制

### 短期记忆（Session）
- 自动保存在 `~/.openclaw/agents/<agent>/sessions/`
- 每次对话自动记录
- 定期压缩避免膨胀

### 长期记忆（Memory）
- 手动维护 `MEMORY.md`
- 记录用户偏好、重要决策、经验教训
- 定期回顾和更新

### 人格进化（SOUL.md）
- 根据反馈优化人格定义
- 添加新的能力和约束
- 记录版本变更

---

## 📝 日常维护清单

### 每日
- [ ] 检查 agent 运行状态
- [ ] 查看 Tushare 调用次数
- [ ] 更新每日记忆 (`memory/YYYY-MM-DD.md`)

### 每周
- [ ] 回顾本周分析准确率
- [ ] 更新 MEMORY.md
- [ ] 优化提示词模板

### 每月
- [ ] 评估 agent 表现
- [ ] 调整模型配置
- [ ] 清理过期会话

---

## 🔧 常见问题

### Q1: Agent 不响应？
**检查**：
- Gateway 是否运行：`openclaw gateway status`
- Agent 配置是否正确：`openclaw agents list`
- 路由规则是否配置

### Q2: Tushare 调用失败？
**检查**：
- Token 是否正确配置
- 积分是否充足
- 调用频率是否超限

### Q3: 分析结果不准确？
**优化**：
- 更新提示词模板
- 调整模型参数（temperature 等）
- 补充更多上下文数据

---

## 📚 参考文档

- TradingAgents-CN 平台：http://localhost:9981
- OpenClaw 文档：https://docs.openclaw.ai
- Tushare 文档：https://tushare.pro/document/2
- TradingAgents-CN 教程：`D:\BaiduNetdisk\LocalBackup\08-Courses\F-LobsterAI\`

---

*配置完成日期：2026-03-17*
*下次回顾日期：2026-03-24*
