# TOOLS.md - 风险分析师的本地配置

## 📊 风险分析工具

### ✅ 已开发工具

| 工具 | 状态 | 说明 |
|------|------|------|
| **风险评分模型** | ✅ 完成 | `scripts/risk_scorer.py` - 综合风险评估 |
| **仓位计算器** | ✅ 完成 | `scripts/position_calculator.py` - 仓位优化计算 |
| **止损止盈计算器** | ✅ 完成 | `scripts/stoploss_calculator.py` - 止损止盈策略 |
| **配置管理** | ✅ 完成 | `scripts/config.py` - 配置统一管理 |

### ⚠️ 数据源配置状态

| 数据源 | 状态 | 推荐方案 |
|--------|------|----------|
| **股票数据 API** | ❌ 待配置 | Tushare (A 股) / AKShare (免费) / Yahoo Finance (美股) |
| **财务数据源** | ❌ 待配置 | Tushare / Wind / Choice |
| **宏观经济指标** | ❌ 待配置 | 国家统计局 / 央行 / Wind |

### 🔧 配置方法

编辑 `config/settings.json` 文件，填入 API 密钥：

```json
{
  "data_sources": {
    "stock_api": {
      "enabled": true,
      "provider": "tushare",
      "api_key": "YOUR_API_KEY",
      "endpoint": "https://api.tushare.pro"
    }
  }
}
```

---

## 📁 文件路径

### 书库
- 金融投资书库：`E:\BaiduSyncdisk\`
- 重点目录：
  - `01-投资基础\` —— 基础理论
  - `金融投资\` —— 投资策略
  - `金融历史\` —— 历史案例

### 工作区
- 根目录：`G:\trading-agents\risk-analyst\`
- 脚本目录：`scripts/`
- 配置目录：`config/`
- 记忆目录：`memory/`
- 长期记忆：`MEMORY.md`

---

## ⚙️ 系统配置

### 风险阈值（默认）
| 等级 | 评分范围 | 仓位建议 |
|------|----------|----------|
| 🔴 高风险 | ≥70 | 0-10% |
| 🟠 中高风险 | 50-69 | <20% |
| 🟡 中等风险 | 30-49 | 20-50% |
| 🟢 低风险 | <30 | 50-80% |
| 🔵 极低风险 | 0 | 80%+ |

### 仓位限制（默认）
- 单只股票上限：30%
- 单一行业上限：50%
- 最大总仓位：80%

### 止损策略（默认）
- 固定比例止损：-5% / -8% / -10%
- 时间止损：10 日
- 移动止损：5% 回撤

---

## 🧪 工具测试

运行以下命令测试工具：

```bash
# 测试风险评分模型
python scripts/risk_scorer.py

# 测试仓位计算器
python scripts/position_calculator.py

# 测试止损止盈计算器
python scripts/stoploss_calculator.py

# 检查配置状态
python scripts/config.py
```

---

## 📝 下一步

1. **配置数据源** - 申请 Tushare/AKShare API 密钥
2. **实战演练** - 对具体股票进行风险评估
3. **持续优化** - 根据实战反馈调整模型参数

---

*最后更新：2026-03-18 | 风险分析师 v3.0 Pro*
