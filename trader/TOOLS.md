# TOOLS.md - 本地配置

**版本**: v1.0  
**最后更新**: 2026-03-18  
**状态**: ✅ 已完成

---

## 🏢 团队环境

### 文骐致远 (Wenqi Zhiyuan)
- **公司名**: 文骐致远
- **使命**: 建立系统的经济学知识体系，实现终生学习与迭代成长
- **愿景**: 成为知行合一的价值投资者
- **价值观**: 长期主义 · 持续学习 · 知行合一 · 系统思维

---

## 👤 用户信息

| 项目 | 配置 |
|------|------|
| **姓名** | 榆哥 |
| **称呼** | 榆哥 |
| **时区** | Asia/Shanghai (GMT+8) |
| **语言** | 中文 |

---

## 🖥️ 系统环境

### 主机信息
| 项目 | 值 |
|------|-----|
| **OS** | Windows 10.0.26200 (x64) |
| **Node.js** | v24.13.1 |
| **OpenClaw** | 2026.3.13 |
| **Shell** | PowerShell |

### 工作空间
- **主工作区**: `G:\trading-agents\trader`
- **书库目录**: `E:\BaiduSyncdisk`
- **配置目录**: `C:\Users\汇语读书\.openclaw`

---

## 📡 通道配置

| 通道 | 状态 | 配置 |
|------|------|------|
| **QQ Bot** | ✅ 启用 | AppID: 1903059548 |
| **DingTalk** | ✅ 启用 | ClientID: ding8ryiqup9fygqoxro |
| **Feishu** | ✅ 启用 | AppID: cli_a93b27220db89cd6 |
| **iMessage** | ❌ 禁用 | - |

### Feishu 配置
- **默认群组**: `oc_d7a2b237fdfc9a74efb23b1a112141e1`
- **群组策略**: `allowlist` (安全模式)
- **连接模式**: WebSocket

### DingTalk 配置
- **DM 策略**: `pairing` (安全模式)

### QQ Bot 配置
- **DM 策略**: `pairing` (安全模式)

---

## 🤖 Agent 团队 (17 个)

### 投资分析部
| Agent ID | 名称 | Emoji | 工作空间 |
|----------|------|-------|----------|
| `market-analyst` | 市场分析师 | 📊 | G:\trading-agents\market-analyst |
| `fundamental-analyst` | 基本面分析师 | 💰 | G:\trading-agents\fundamental-analyst |
| `technical-analyst` | 技术分析师 | 📈 | G:\trading-agents\technical-analyst |
| `news-analyst` | 新闻分析师 | 📰 | G:\trading-agents\news-analyst |
| `sentiment-analyst` | 情绪分析师 | 😊 | G:\trading-agents\sentiment-analyst |
| `risk-analyst` | 风险分析师 | ⚠️ | G:\trading-agents\risk-analyst |
| `portfolio-manager` | 组合经理 | 💼 | G:\trading-agents\portfolio-manager |
| `trading-manager` | 交易经理 | 🎯 | G:\trading-agents\trading-manager |
| `trader` | 交易员 | 💹 | G:\trading-agents\trader |
| `post-processor` | 报告生成 | 📄 | G:\trading-agents\post-processor |
| `research-lead` | 研究主管 | 🔬 | G:\trading-agents\research-lead |
| `researcher-1` | 行业研究员 | 🏭 | G:\trading-agents\researcher-1 |
| `researcher-2` | 公司研究员 | 🏢 | G:\trading-agents\researcher-2 |
| `trade-executor` | 交易执行助手 | ✅ | G:\trading-agents\trade-executor |
| `economic-library` | 经济书库助手 | 📚 | G:\trading-agents\economic-library |

### 其他 Agent
| Agent ID | 名称 | 工作空间 |
|----------|------|----------|
| `main` | 愉哥 | - |
| `dmgj_v1` | 电脑管理助手 v1.0.0 | G:\dmgj_v1 |

---

## 🧠 模型配置

### 主模型
- **Provider**: qwen / aliyun
- **Model**: qwen3.5-plus
- **Context**: 200k tokens
- **Reasoning**: 支持

### API 配置
- **Base URL**: https://coding.dashscope.aliyuncs.com/v1
- **API Key**: sk-sp-9fe8ea992fa54e5bb2767ebe7ff3392b

---

## 📚 书库资源

### 百度书库 (E:\BaiduSyncdisk)
| 目录 | 用途 |
|------|------|
| `00-Inbox` | 待处理文件 |
| `01-Foundation 基础阶段` | 基础学习材料 |
| `02-Intermediate 中级阶段` | 进阶学习材料 |
| `03-Advanced 专业阶段` | 专业学习材料 |
| `04-Mastery 大师阶段` | 高级学习材料 |
| `05-Skills 实战技能` | 实战技能材料 |
| `06-Reference 参考资料` | 参考资料 |
| `shared-archive` | 共享档案库 |
| `_Output` | 输出目录 |

### 共享档案库
- **学习总结**: `E:\BaiduSyncdisk\shared-archive\learning\`
- **通知板**: `E:\BaiduSyncdisk\shared-archive\notice-board\`
- **核心备份**: `E:\BaiduSyncdisk\shared-archive\library\core-backup\`

---

## 🛠️ 外部系统

### TradingAgents-CN 平台
- **用途**: 投资分析平台
- **状态**: 已配置
- **数据源**: Tushare (已购 1000 元积分)

### Tushare 配置
- **积分**: 10120 分
- **实时数据**: 已开启
- **缓存 TTL**: 60 秒

### LobsterAI
- **用途**: 电子书库处理
- **技能**: PDF/XLSX/DOCX 处理等 18 个技能

### ClawPanel
- **用途**: 系统监控
- **状态**: 轻量级运行中

---

## 🔒 安全配置 (已修复)

| 配置项 | 值 | 说明 |
|--------|-----|------|
| `channels.feishu.groupPolicy` | `allowlist` | 白名单模式 |
| `channels.feishu.groupAllowlist` | `[oc_d7a2b237fdfc9a74efb23b1a112141e1]` | 仅允许默认群组 |
| `channels.dingtalk-connector.dmPolicy` | `pairing` | 配对模式 |
| `channels.qqbot.dmPolicy` | `pairing` | 配对模式 |
| `gateway.controlUi.allowedOrigins` | 移除 `*` | 仅允许本地来源 |

---

## 📝 本地笔记

### 交易偏好
- **投资风格**: 价值投资
- **持仓周期**: 中长期 (3-5 年+)
- **风险偏好**: 中等
- **最大回撤容忍**: 15%

### 沟通偏好
- **语言风格**: 专业但不生硬，简洁有温度
- **汇报频率**: 重要事项实时汇报，日常工作定期总结
- **决策方式**: 提供专业建议，最终决策由用户决定

### 工作时间
- **晨会**: 09:00
- **午评**: 12:00
- **晚报**: 20:00
- **备份**: 23:00

---

## 🔗 重要链接

| 资源 | URL |
|------|-----|
| OpenClaw 文档 | https://docs.openclaw.ai |
| OpenClaw 社区 | https://discord.com/invite/clawd |
| ClawHub 技能 | https://clawhub.com |
| Tushare 官网 | https://tushare.pro |
| 巨潮资讯 | http://www.cninfo.com.cn |

---

## 📞 紧急联系

### 系统问题
1. 检查 Gateway 状态：`openclaw gateway status`
2. 查看日志：`openclaw logs --follow`
3. 安全审计：`openclaw security audit`
4. 重启 Gateway：`openclaw gateway restart`

### 配置问题
1. 查看配置：`openclaw config.get`
2. 配置修复：使用 `gateway.config.patch`
3. 版本检查：`openclaw --version`

---

*TOOLS.md - 本地配置速查表*  
**版本**: v1.0  
**最后更新**: 2026-03-18  
*维护者：交易员 💹*
