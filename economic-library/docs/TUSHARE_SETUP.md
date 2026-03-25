# Tushare API 集成指南

## 📋 概述

经济书库已集成 Tushare Pro API，用于获取 A 股市场数据。

**文档**: https://tushare.pro/document/2  
**Token**: 已配置 (eb0a4fb1***)

---

## 🔧 配置说明

### 1. 环境变量 (.env)

```bash
# Tushare API Token
TUSHARE_TOKEN=eb0a4fb17ede71c5d34a3eca96758681b31af97f0ade9f0a3711e877

# Tushare API Base URL
TUSHARE_BASE_URL=https://api.tushare.pro

# 数据缓存配置
CACHE_DIR=data/cache
CACHE_EXPIRY_HOURS=24
```

### 2. 持仓配置 (config/holdings.json)

```json
{
  "holdings": [
    {
      "ts_code": "000001.SZ",
      "name": "平安银行",
      "shares": 1000,
      "cost_price": 10.50,
      "notes": "示例持仓"
    }
  ],
  "watchlist": [
    {
      "ts_code": "600519.SH",
      "name": "贵州茅台",
      "notes": "关注中"
    }
  ]
}
```

### 3. Python 依赖

```bash
pip install -r requirements.txt
```

---

## 📊 可用脚本

### 1. 市场数据获取

```bash
python scripts/tushare_daily_report.py
```

**功能**:
- 获取大盘指数 (上证/深证/创业板)
- 获取市场概况 (换手率/市盈率/市值等)
- 输出到 `data/tushare_daily_YYYY-MM-DD.json`

### 2. 价格预警检查

```bash
python scripts/price_alert.py
```

**功能**:
- 检查持仓股票盈亏
- 触发止损/止盈/预警警报
- 输出到 `alerts/price_alerts_YYYY-MM-DD_HH-MM.json`

**预警级别**:
- 🚨 止损：≤ -7%
- 🎯 止盈：≥ +20%
- ⚠️ 预警：≤ -3%

### 3. 持仓监控日报

```bash
python scripts/portfolio_monitor.py
```

**功能**:
- 计算总投入/总市值/总盈亏
- 找出涨跌 TOP3 股票
- 输出到 `reports/portfolio_YYYY-MM-DD.json`

### 4. 投资日报生成

```bash
python scripts/generate_daily_report.py
```

**功能**:
- 基于 Tushare 数据生成 Markdown 日报
- 输出到 `reports/daily_report_YYYY-MM-DD.md`

---

## 🔌 API 模块使用

### 直接调用 API

```python
from scripts.tushare_api import TushareAPI, get_market_data

# 方法 1: 使用便捷函数
data = get_market_data()
print(data)

# 方法 2: 使用 API 类
api = TushareAPI()

# 获取大盘指数
indices = api.get_index_daily(ts_code="000001.SH", trade_date="20260321")

# 获取每日大盘指标
basic = api.get_daily_basic(trade_date="20260321")

# 获取股票列表
stocks = api.get_stock_list()
```

### 常用指数代码

| 指数 | 代码 | 名称 |
|------|------|------|
| 上证指数 | 000001.SH | 上海证券综合指数 |
| 深证成指 | 399001.SZ | 深圳成份指数 |
| 创业板指 | 399006.SZ | 创业板指数 |
| 沪深 300 | 000300.SH | 沪深 300 指数 |
| 中证 500 | 000905.SH | 中证 500 指数 |

---

## ⚙️ Cron 任务配置

已配置的自动化任务：

| 任务 | 频率 | 脚本 |
|------|------|------|
| 投资日报自动生成 | 工作日 09:00 | tushare_daily_report.py + generate_daily_report.py |
| 价格预警检查 | 每小时 | price_alert.py |
| 持仓监控日报 | 工作日 15:30 | portfolio_monitor.py |

---

## 🔍 故障排查

### 1. Token 无效

```
错误：Tushare API 错误：token 无效或已过期
解决：检查.env 文件中的 TUSHARE_TOKEN 是否正确
```

### 2. 权限不足

```
错误：Tushare API 错误：您没有权限访问此接口
解决：部分接口需要积分，查看 https://tushare.pro/user/point
```

### 3. 网络超时

```
错误：网络请求失败：Connection timed out
解决：检查网络连接，Tushare 服务器在国内
```

### 4. 数据为空

```
警告：获取 XXX 数据失败
解决：可能是非交易日，或股票代码错误
```

---

## 📚 扩展阅读

- [Tushare 官方文档](https://tushare.pro/document/2)
- [Tushare 积分制度](https://tushare.pro/user/point)
- [A 股交易日历](https://tushare.pro/document/2?doc_id=24)

---

*最后更新：2026-03-21*  
*版本：v1.0*
