# TradingAgents-CN 工具配置完全指南

> 配置日期：2026-03-17  
> 平台版本：TradingAgents-CN v2.0.0  
> 数据源：Tushare Pro + 多数据源

---

## 📊 工具分类总览

TradingAgents-CN 平台提供以下工具类别：

| 分类 | 工具数量 | 数据源 | 用途 |
|------|----------|--------|------|
| 📈 市场数据 | 12+ | tushare/yfinance | 股票行情、指数数据、资金流向 |
| 📊 基本面数据 | 6+ | finnhub/simfin | 财务报表、估值指标 |
| 📰 新闻数据 | 6+ | finnhub/google/reddit | 财经新闻、宏观新闻 |
| 😊 社交媒体 | 3+ | reddit/twitter/chinese_social | 市场情绪分析 |
| 📉 技术分析 | 3+ | stockstats/multiple | 技术指标计算 |
| 🇨🇳 中国市场 | 8+ | tushare | A 股专属数据 |
| 📋 复盘分析 | 5+ | database/internal | 交易记录、持仓分析 |

---

## 🔧 核心工具详解

### 1. 📈 统一市场数据 (`get_stock_market_data_unified`)

**用途**：获取统一格式的股票市场数据

**数据源**：yfinance/tushare（自动切换）

**参数**：
```json
{
  "ticker": "000001.SZ",      // 股票代码（必填）
  "start_date": "20260317",   // 开始日期（必填）
  "end_date": "20260317"      // 结束日期（必填）
}
```

**返回数据**：
```json
{
  "ticker": "000001.SZ",
  "company_name": "平安银行",
  "current_price": 12.35,
  "change_pct": 1.23,
  "volume": 1234567,
  "amount": 15234567890,
  "high": 12.50,
  "low": 12.20,
  "open": 12.30,
  "pre_close": 12.20,
  "history": [...]
}
```

**使用场景**：
- 市场分析师获取日线数据
- 技术分析师获取 K 线数据
- 所有需要股价数据的分析

---

### 2. 📊 统一基本面数据 (`get_stock_fundamentals_unified`)

**用途**：获取公司基本面数据的统一接口

**数据源**：finnhub/simfin

**参数**：
```json
{
  "ticker": "000001.SZ",
  "period": "20251231"
}
```

**返回数据**：
```json
{
  "ticker": "000001.SZ",
  "period": "20251231",
  "revenue": 123456789000,
  "net_profit": 23456789000,
  "roe": 12.34,
  "gross_margin": 34.56,
  "debt_ratio": 45.67,
  "pe_ttm": 8.5,
  "pb": 0.9,
  "total_mv": 234567890000
}
```

**使用场景**：
- 基本面分析师财务分析
- 估值建模
- 股票筛选

---

### 3. 📰 统一新闻数据 (`get_stock_news_unified`)

**用途**：获取股票相关新闻的统一接口

**数据源**：finnhub/google

**参数**：
```json
{
  "ticker": "000001.SZ",
  "start_date": "20260301",
  "end_date": "20260317",
  "limit": 20
}
```

**返回数据**：
```json
{
  "news": [
    {
      "title": "平安银行 2025 年净利润增长 10%",
      "source": "证券时报",
      "publish_time": "2026-03-17 09:30:00",
      "summary": "...",
      "sentiment": "positive"
    }
  ]
}
```

**使用场景**：
- 新闻分析师收集资讯
- 情绪分析
- 事件驱动分析

---

### 4. 📉 统一技术指标分析 (`get_technical_indicators`)

**用途**：获取股票的各类技术指标

**数据源**：multiple（多数据源）

**支持指标**：
- MACD（平滑异同移动平均线）
- RSI（相对强弱指标）
- KDJ（随机指标）
- BOLL（布林带）
- MA（移动平均线）
- EMA（指数平均线）

**参数**：
```json
{
  "ticker": "000001.SZ",
  "indicators": ["MACD", "RSI", "KDJ", "BOLL"],
  "period": "daily"
}
```

**使用场景**：
- 技术分析师深度分析
- 量化策略回测
- 买卖信号识别

---

### 5. 🇨🇳 中国市场概览 (`get_china_market_overview`)

**用途**：获取中国股市主要指数行情概览

**数据源**：tushare

**覆盖指数**：
- 上证指数 (000001.SH)
- 深证成指 (399001.SZ)
- 创业板指 (399006.SZ)
- 科创 50 (000688.SH)

**返回数据**：
```json
{
  "indices": [
    {
      "code": "000001.SH",
      "name": "上证指数",
      "close": 3250.50,
      "change_pct": 0.85,
      "volume": 234567890,
      "amount": 345678901234
    }
  ]
}
```

**使用场景**：
- 大盘分析师评估市场环境
- 开盘/收盘简报
- 市场情绪判断

---

### 6. 💰 北向资金流向 (`get_north_flow`)

**用途**：获取沪深港通北向资金流向数据

**数据源**：tushare

**参数**：
```json
{
  "start_date": "20260301",
  "end_date": "20260317"
}
```

**使用场景**：
- 资金面分析
- 外资动向监控
- 市场情绪判断

---

### 7. 📊 两融余额 (`get_margin_trading`)

**用途**：获取融资融券余额数据

**数据源**：tushare

**使用场景**：
- 杠杆资金分析
- 市场热度评估
- 风险预警

---

### 8. 📈 涨跌停统计 (`get_limit_stats`)

**用途**：获取涨跌停家数和涨跌家数统计

**数据源**：tushare

**使用场景**：
- 市场情绪评估
- 赚钱效应分析
- 极端行情预警

---

### 9. 🔄 市场周期识别 (`identify_market_cycle`)

**用途**：识别当前市场所处的周期阶段

**数据源**：tushare

**周期阶段**：
- 牛市初期
- 牛市中期
- 牛市末期
- 熊市初期
- 熊市中期
- 熊市末期
- 震荡市

**使用场景**：
- 战略资产配置
- 仓位控制参考
- 长期投资决策

---

### 10. 📊 板块数据 (`get_sector_data`)

**用途**：获取股票所属板块的表现数据

**数据源**：tushare

**使用场景**：
- 行业分析
- 板块轮动监控
- 同业对比

---

### 11. 💰 资金流向 (`get_fund_flow_data`)

**用途**：获取板块资金流向数据

**数据源**：tushare

**使用场景**：
- 主力资金监控
- 热点板块识别
- 资金面分析

---

### 12. 📈 同业对比 (`get_peer_comparison`)

**用途**：获取同行业股票对比数据

**数据源**：tushare

**对比维度**：
- 估值指标（PE/PB/PS）
- 盈利能力（ROE/毛利率/净利率）
- 成长能力（营收增长/利润增长）
- 规模指标（市值/营收/净利润）

**使用场景**：
- 个股相对价值分析
- 行业地位评估
- 选股参考

---

## 🛠️ 工具配置步骤

### 方式 1：通过 TradingAgents-CN 平台配置

1. 访问 http://localhost:9981/workflow/tools
2. 点击要配置的工具"详情"
3. 配置数据源优先级
4. 设置 API Token（如 Tushare Token）
5. 测试工具调用
6. 保存配置

### 方式 2：通过配置文件

编辑 `~/.openclaw/trading-tools-config.json`：

```json
{
  "data_sources": {
    "tushare": {
      "enabled": true,
      "token": "你的 tushare token",
      "priority": 1
    },
    "yfinance": {
      "enabled": true,
      "priority": 2
    },
    "finnhub": {
      "enabled": true,
      "api_key": "你的 finnhub api key",
      "priority": 1
    }
  },
  "tool_overrides": {
    "get_stock_market_data_unified": {
      "preferred_source": "tushare",
      "fallback_source": "yfinance"
    }
  }
}
```

---

## 🔑 Tushare Token 配置

### 获取 Token

1. 访问 https://tushare.pro
2. 注册账号
3. 进入个人中心 → 接口 TOKEN
4. 复制 Token

### 配置 Token

**方式 1：环境变量（推荐）**
```powershell
# PowerShell - 用户级别
[Environment]::SetEnvironmentVariable("TUSHARE_TOKEN", "你的 token", "User")

# 验证
echo $env:TUSHARE_TOKEN
```

**方式 2：平台配置**
1. 访问 http://localhost:9981/settings
2. 数据源配置 → Tushare
3. 粘贴 Token
4. 保存并测试

**方式 3：配置文件**
在 `~/.openclaw/tushare_config.json` 中：
```json
{
  "token": "你的 tushare token"
}
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

## 📊 工具调用示例

### 示例 1：市场分析师获取日线数据

```python
# 调用统一市场数据工具
result = await tools.get_stock_market_data_unified(
    ticker="000001.SZ",
    start_date="20260317",
    end_date="20260317"
)

# 生成分析报告
report = f"""
# 平安银行 (000001.SZ) 市场分析报告

## 核心数据
- 当前价格：{result['current_price']} 元
- 涨跌幅：{result['change_pct']}%
- 成交量：{result['volume']} 手
- 成交额：{result['amount']} 元

## 价格区间
- 最高：{result['high']} 元
- 最低：{result['low']} 元
- 开盘：{result['open']} 元
"""
```

### 示例 2：基本面分析师获取财务数据

```python
# 获取基本面数据
fundamentals = await tools.get_stock_fundamentals_unified(
    ticker="000001.SZ",
    period="20251231"
)

# 计算估值指标
pe = fundamentals['pe_ttm']
pb = fundamentals['pb']
roe = fundamentals['roe']

# 估值分析
if pe < 10:
    valuation = "低估"
elif pe < 20:
    valuation = "合理"
else:
    valuation = "高估"

report = f"""
# 平安银行基本面分析

## 估值水平
- PE(TTM): {pe} → {valuation}
- PB: {pb}
- ROE: {roe}%
"""
```

### 示例 3：技术分析师获取技术指标

```python
# 获取技术指标
technicals = await tools.get_technical_indicators(
    ticker="000001.SZ",
    indicators=["MACD", "RSI", "KDJ", "BOLL"],
    period="daily"
)

# 技术分析
macd_signal = technicals['MACD']['signal']  # 金叉/死叉
rsi_value = technicals['RSI']['value']      # 超买/超卖

report = f"""
# 平安银行技术分析

## MACD
- 信号：{macd_signal}
- DIF: {technicals['MACD']['dif']}
- DEA: {technicals['MACD']['dea']}

## RSI
- 数值：{rsi_value}
- 状态：{'超买' if rsi_value > 70 else '超卖' if rsi_value < 30 else '中性'}
"""
```

---

## ⚠️ 注意事项

### 1. Token 安全
- ❌ 不要将 Token 提交到代码仓库
- ❌ 不要在公开场合分享 Token
- ✅ 使用环境变量存储 Token
- ✅ 定期更换 Token

### 2. 调用限制
- Tushare 有积分限制（根据积分等级）
- 建议缓存已获取的数据
- 避免重复调用相同接口
- 批量获取数据时使用日期范围

### 3. 数据质量
- 验证返回数据是否为空
- 处理异常情况（网络错误、API 限流等）
- 多数据源 fallback 机制
- 记录数据获取日志

### 4. 错误处理
```python
try:
    data = await tools.get_stock_market_data_unified(...)
except Exception as e:
    logger.error(f"获取数据失败：{e}")
    # 尝试备用数据源
    data = await tools.get_stock_market_data_unified(
        ..., 
        source="yfinance"  # 切换到 yfinance
    )
```

---

## 📚 参考文档

- TradingAgents-CN 平台：http://localhost:9981
- Tushare 文档：https://tushare.pro/document/2
- 本地教程：`D:\BaiduNetdisk\LocalBackup\08-Courses\F-TradingAgents-CN\07-Tushare 股票筛选使用指南.md`

---

*最后更新：2026-03-17*
