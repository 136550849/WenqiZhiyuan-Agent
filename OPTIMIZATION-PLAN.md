# 🦞 OpenClaw Agent 配置优化方案

> 优化日期：2026-03-17 02:13  
> 参考平台：TradingAgents-CN v2.0.0  
> 优化目标：对齐平台配置 + 提升分析质量

---

## 📊 当前配置状态

### OpenClaw Agent（13 个）
✅ 已配置：
- market-analyst（市场分析师 📊）
- fundamental-analyst（基本面分析师 💰）
- technical-analyst（技术分析师 📈）
- news-analyst（新闻分析师 📰）
- sentiment-analyst（情绪分析师 😊）
- risk-analyst（风险分析师 ⚠️）
- portfolio-manager（组合经理 💼）
- trading-manager（交易经理 🎯）
- research-lead（研究主管 🔬）
- researcher-1（行业研究员 🏭）
- researcher-2（公司研究员 🏢）
- trader（交易员 💹）
- post-processor（报告生成 📄）

### TradingAgents-CN Agent（23 个）
- 分析师（13）：市场、基本面、新闻、社交媒体、大盘、板块、技术面等
- 研究员（2）：看涨研究员、看跌研究员
- 交易员（1）：交易员
- 风险管理（3）：激进/保守/中性风险分析师
- 管理者（4）：研究经理、风险管理者等
- 后处理器（0）

---

## 🎯 优化方向

### 1. 提示词优化（Prompt Engineering）

#### 市场分析师（market-analyst）
**当前**：基础技术分析
**优化后**：
```markdown
# 角色定位
你是一位专业的股票技术分析师，专注于 A 股市场。

# 工作流程
1. 获取数据：调用 get_stock_market_data_unified 工具
2. 趋势分析：判断大趋势（上升/下降/震荡）
3. K 线形态：识别关键 K 线组合
4. 技术指标：MACD、RSI、KDJ、布林带
5. 支撑阻力：识别关键价位
6. 成交量：分析量价关系
7. 生成报告：结构化输出

# 分析框架
## 趋势判断
- 长期趋势（200 日均线）
- 中期趋势（60 日均线）
- 短期趋势（20 日均线）

## K 线形态
- 单 K 线：阳线/阴线/十字星
- K 线组合：早晨之星/黄昏之星/吞没形态
- 缺口分析

## 技术指标
| 指标 | 数值 | 信号 | 说明 |
|------|------|------|------|
| MACD | | 金叉/死叉 | |
| RSI | | 超买/超卖 | |
| KDJ | | 金叉/死叉 | |

## 支撑阻力
- 支撑位 1/2/3
- 阻力位 1/2/3

## 成交量
- 量比
- 量价关系

# 输出要求
- 使用中文
- 基于真实数据
- 结构清晰
- 包含风险提示
```

#### 基本面分析师（fundamental-analyst）
**优化重点**：
- 增加杜邦分析
- 增加现金流分析
- 增加同业对比
- 增加估值建模

#### 交易经理（trading-manager）
**优化重点**：
- 增加决策矩阵
- 增加置信度评估
- 增加情景分析
- 增加备选方案

---

### 2. 模型配置优化

#### 当前配置
```json
{
  "model": "qwen/qwen3.5-plus"
}
```

#### 优化建议
根据分析深度选择模型：

| 分析类型 | 推荐模型 | 说明 |
|----------|----------|------|
| 快速分析 | qwen/qwen-turbo | 响应快，成本低 |
| 标准分析 | qwen/qwen3.5-plus | 平衡性能和成本 |
| 深度分析 | qwen/qwen-max | 最强性能，复杂任务 |
| 财务报告 | qwen/qwen-max-2026-01-23 | 擅长财务分析 |

#### 配置示例
```json
{
  "agents": {
    "list": [
      {
        "id": "market-analyst",
        "model": "qwen/qwen3.5-plus",
        "models": {
          "quick": "qwen/qwen-turbo",
          "standard": "qwen/qwen3.5-plus",
          "deep": "qwen/qwen-max"
        }
      }
    ]
  }
}
```

---

### 3. 工具配置优化

#### 当前工具
- get_stock_market_data_unified ✅
- get_financial_data ⏳
- get_technical_indicators ⏳

#### 建议添加
```json
{
  "tools": {
    "allow": [
      "get_stock_market_data_unified",
      "get_stock_fundamentals_unified",
      "get_technical_indicators",
      "get_stock_news_unified",
      "get_china_market_overview",
      "get_north_flow",
      "get_sector_data",
      "get_peer_comparison",
      "identify_market_cycle",
      "web_search",
      "read",
      "write"
    ]
  }
}
```

---

### 4. 会话管理优化

#### 压缩策略
```json
{
  "compaction": {
    "mode": "aggressive",
    "threshold": 50,
    "preserveRecent": 10
  }
}
```

#### 记忆维护
- 每日更新 MEMORY.md
- 每周清理过期会话
- 每月优化提示词

---

### 5. 路由规则优化

#### 当前状态
- Routing rules: 0（未配置）

#### 建议配置
```json
{
  "bindings": [
    {
      "agentId": "trading-manager",
      "match": {
        "channel": "webchat",
        "accountId": "__default__"
      }
    },
    {
      "agentId": "market-analyst",
      "match": {
        "channel": "webchat",
        "accountId": "__default__",
        "textContains": ["技术面", "技术分析", "K 线"]
      }
    },
    {
      "agentId": "fundamental-analyst",
      "match": {
        "channel": "webchat",
        "accountId": "__default__",
        "textContains": ["基本面", "财务", "估值"]
      }
    }
  ]
}
```

---

### 6. 新增 Agent 建议

基于 TradingAgents-CN 的配置，建议新增：

#### 6.1 看涨研究员（bull-researcher）
```json
{
  "id": "bull-researcher",
  "name": "看涨研究员",
  "workspace": "G:\\trading-agents\\bull-researcher",
  "model": "qwen/qwen3.5-plus",
  "identity": {
    "name": "看涨研究员",
    "emoji": "🐂"
  }
}
```

**职责**：从看涨角度综合分析，找出买入理由

#### 6.2 看跌研究员（bear-researcher）
```json
{
  "id": "bear-researcher",
  "name": "看跌研究员",
  "workspace": "G:\\trading-agents\\bear-researcher",
  "model": "qwen/qwen3.5-plus",
  "identity": {
    "name": "看跌研究员",
    "emoji": "🐻"
  }
}
```

**职责**：从看跌角度综合分析，找出风险因素

#### 6.3 时机分析师（timing-analyst）
```json
{
  "id": "timing-analyst",
  "name": "时机分析师",
  "workspace": "G:\\trading-agents\\timing-analyst",
  "model": "qwen/qwen3.5-plus",
  "identity": {
    "name": "时机分析师",
    "emoji": "⏰"
  }
}
```

**职责**：分析买入卖出时机

#### 6.4 仓位分析师（position-analyst）
```json
{
  "id": "position-analyst",
  "name": "仓位分析师",
  "workspace": "G:\\trading-agents\\position-analyst",
  "model": "qwen/qwen3.5-plus",
  "identity": {
    "name": "仓位分析师",
    "emoji": "📊"
  }
}
```

**职责**：分析仓位控制和加减仓策略

---

## 🔧 优化实施步骤

### 阶段 1：提示词优化（1-2 天）
- [ ] 优化 market-analyst SOUL.md
- [ ] 优化 fundamental-analyst SOUL.md
- [ ] 优化 trading-manager SOUL.md
- [ ] 为所有 agent 创建 AGENTS.md

### 阶段 2：模型配置（1 天）
- [ ] 配置多模型支持
- [ ] 设置模型切换规则
- [ ] 测试不同模型效果

### 阶段 3：工具集成（1-2 天）
- [ ] 集成更多 Tushare 工具
- [ ] 配置工具调用权限
- [ ] 测试工具调用

### 阶段 4：路由配置（1 天）
- [ ] 配置消息路由规则
- [ ] 测试路由准确性
- [ ] 优化匹配条件

### 阶段 5：新增 Agent（2-3 天）
- [ ] 创建 bull-researcher
- [ ] 创建 bear-researcher
- [ ] 创建 timing-analyst
- [ ] 创建 position-analyst

---

## 📈 效果评估

### 评估指标
| 指标 | 当前 | 目标 | 说明 |
|------|------|------|------|
| 分析准确率 | - | >80% | 与实际情况对比 |
| 响应时间 | - | <30 秒 | 从请求到输出 |
| 报告质量 | - | 4.5/5 | 用户评分 |
| 工具调用成功率 | - | >95% | API 调用成功 |
| 用户满意度 | - | >90% | 用户反馈 |

### 测试方法
1. 历史回测：用历史数据测试分析准确性
2. 对比测试：不同配置对比效果
3. 用户测试：收集用户反馈

---

## 📚 参考配置

### TradingAgents-CN 配置
- 市场分析师 v2.0
- 基本面分析师 v2.0
- 技术面分析师 v2.0
- 研究经理 v2.0
- 风险管理者 v2.0

### OpenClaw 最佳实践
- 使用 SOUL.md 定义人格
- 使用 AGENTS.md 定义行为准则
- 使用 MEMORY.md 记录经验
- 定期更新优化

---

## 🎯 下一步行动

### 立即可做
1. 优化 market-analyst 提示词
2. 配置模型切换规则
3. 测试工具调用

### 本周完成
1. 完成所有 agent 的 AGENTS.md
2. 配置路由规则
3. 测试新增 agent

### 持续优化
1. 根据反馈调整提示词
2. 监控分析质量
3. 更新模型配置

---

*优化方案版本：v1.0*  
*制定日期：2026-03-17 02:13*  
*下次回顾：2026-03-24*
