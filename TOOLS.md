# TOOLS.md - 交易 Agent 工具配置

## Tushare 数据接口配置

### 安装 Tushare

```bash
pip install tushare
```

### 配置 Token

**方式 1：环境变量（推荐）**
```powershell
# PowerShell - 用户级别
[Environment]::SetEnvironmentVariable("TUSHARE_TOKEN", "你的 token", "User")

# PowerShell - 系统级别
[Environment]::SetEnvironmentVariable("TUSHARE_TOKEN", "你的 token", "Machine")
```

**方式 2：配置文件**
在 `~/.openclaw/tushare_config.json` 中存储：
```json
{
  "token": "你的 tushare token"
}
```

### Tushare 工具函数

#### 1. 获取股票基本信息
```python
import tushare as ts

pro = ts.pro_api('你的 token')

# 股票列表
stock_basic = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,market,list_date')

# 单个股票信息
stock_info = pro.stock_company(ts_code='000001.SZ', fields='ts_code,change_date,scope,reg_capital')
```

#### 2. 获取日线数据
```python
# 日线行情
daily = ts.pro_daily(ts_code='000001.SZ', start_date='20250101', end_date='20260317')

# 复权数据
adj_factor = ts.pro_adj_factor(ts_code='000001.SZ', trade_date='20260317')
```

#### 3. 获取财务指标
```python
# 主要财务指标
fina_indicator = ts.pro_fina_indicator(ts_code='000001.SZ', period='20251231')

# 利润表
income = ts.pro_income(ts_code='000001.SZ', period='20251231')

# 资产负债表
balancesheet = ts.pro_balsheet(ts_code='000001.SZ', period='20251231')

# 现金流量表
cashflow = ts.pro_cashflow(ts_code='000001.SZ', period='20251231')
```

#### 4. 获取指数数据
```python
# 大盘指数
index_daily = ts.pro_index_daily(ts_code='000001.SH', start_date='20250101', end_date='20260317')

# 指数成分股
index_weight = ts.pro_index_weight(index_code='000001.SH', start_date='20260301', end_date='20260317')
```

#### 5. 获取新闻数据
```python
# 个股新闻
news = ts.pro_news(ts_code='000001.SZ', start_date='20260301', end_date='20260317')

# 财经新闻
top_news = ts.pro_top_news(start_date='20260317', end_date='20260317')
```

#### 6. 获取资金流向
```python
# 个股资金流向
moneyflow = ts.pro_moneyflow(ts_code='000001.SZ', start_date='20260301', end_date='20260317')

# 北向资金
north_flow = ts.pro_north_daily(start_date='20260301', end_date='20260317')
```

---

## OpenClaw 工具封装

### get_stock_market_data_unified

**功能**：获取统一格式的股票市场数据

**参数**：
- `ticker` (必填): 股票代码，如 `000001.SZ`
- `start_date` (必填): 开始日期，如 `20260317`
- `end_date` (必填): 结束日期，如 `20260317`

**返回**：
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
  "history": [
    {
      "trade_date": "20260317",
      "close": 12.35,
      "open": 12.30,
      "high": 12.50,
      "low": 12.20,
      "volume": 1234567,
      "amount": 15234567890
    }
  ]
}
```

### get_financial_data

**功能**：获取财务指标数据

**参数**：
- `ticker` (必填): 股票代码
- `period` (可选): 报告期，如 `20251231`

**返回**：
```json
{
  "ticker": "000001.SZ",
  "period": "20251231",
  "revenue": 123456789000,
  "net_profit": 23456789000,
  "roe": 12.34,
  "gross_margin": 34.56,
  "debt_ratio": 45.67,
  ...
}
```

---

## 使用示例

### 市场分析师调用示例

```python
# 在 agent 中调用工具
result = await tools.get_stock_market_data_unified(
    ticker="000001.SZ",
    start_date="20260317",
    end_date="20260317"
)

# 基于结果生成分析报告
report = generate_technical_analysis(result)
```

### 基本面分析师调用示例

```python
# 获取财务数据
financial = await tools.get_financial_data(
    ticker="000001.SZ",
    period="20251231"
)

# 计算估值指标
pe = calculate_pe(financial)
pb = calculate_pb(financial)
```

---

## 注意事项

1. **Token 安全**：不要将 token 提交到代码仓库
2. **调用限制**：Tushare 有积分限制，注意调用频率
3. **数据缓存**：建议缓存已获取的数据，避免重复调用
4. **错误处理**：处理 API 调用失败的情况

---

*最后更新：2026-03-17*
