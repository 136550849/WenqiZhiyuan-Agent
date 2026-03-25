# 📚 深度学习笔记 - TradingAgents-CN 架构

**学习时间**: 2026-03-18 18:45-19:30  
**学习人**: research-lead 🔬  
**资料来源**: D:\BaiduNetdisk\LocalBackup\08-Courses\F-TradingAgents-CN

---

## 🏗️ 平台整体架构

### 技术栈
```
前端 (Vue.js + Element Plus)
  ↓ HTTP/REST API + WebSocket
后端 (FastAPI Python)
  ↓
MongoDB + Redis + 文件存储
```

### 后端目录结构
```
app/
├── routers/ (50+ 路由文件)
│   ├── stocks.py - 股票数据接口
│   ├── analysis.py - 分析任务接口
│   ├── favorites.py - 自选股接口
│   ├── sync.py - 数据同步接口
│   └── reports.py - 分析报告接口
│
├── services/ (业务逻辑层)
│   ├── stock_data_service.py
│   ├── analysis_service.py
│   └── data_sources/ (数据源适配器)
│       ├── base.py
│       ├── tushare_adapter.py
│       ├── akshare_adapter.py
│       └── baostock_adapter.py
│
├── models/ (MongoDB 文档结构)
├── schemas/ (Pydantic 数据验证)
├── core/ (核心配置)
└── utils/ (工具函数)
```

---

## 📊 Tushare API 股票筛选

### 投资 6 大标准筛选条件

| 序号 | 条件 | 标准 | 数据来源 |
|------|------|------|----------|
| 1 | 市值 | > 100 亿 | daily_basic.total_mv |
| 2 | ROE | > 15% | fina_indicator.roe |
| 3 | 营收增长率 | > 20% | income.total_revenue |
| 4 | 净利润增长率 | > 20% | income.n_income_attr_p |
| 5 | 毛利率 | > 30% | income 计算 |
| 6 | 负债率 | < 50% | balancesheet 计算 |

### 计算公式
```python
# 营收增长率
rev_growth = ((current_revenue - prev_revenue) / prev_revenue) * 100

# 净利润增长率
net_growth = ((current_net_profit - prev_net_profit) / prev_net_profit) * 100

# 毛利率
gross_margin = ((revenue - cost) / revenue) * 100

# 负债率
debt_ratio = (total_liab / total_assets) * 100
```

### Tushare API 配置
```python
import tushare as ts

TOKEN = 'eb0a4fb17ede71c5d34a3eca96758681b31af97f0ade9f0a3711e877'
pro = ts.pro_api(TOKEN)

# 获取市值数据
df = pro.daily_basic(ts_code='', trade_date='20260312', 
                     fields='ts_code,total_mv,pe_ttm,pb')

# 获取 ROE 数据
df = pro.fina_indicator(ts_code='002027.SZ', 
                        fields='ts_code,ann_date,roe')
```

---

## 🤖 多智能体架构对比

### TradingAgents-CN
```
多智能体分析引擎
├── 市场分析师 → 技术分析
├── 基本面分析师 → 财务分析
├── 新闻分析师 → 舆情分析
├── 交易员 → 交易策略
├── 风险管理师 → 风险评估
└── 组合管理师 → 投资建议
```

### 我们的系统 (21 Agent)
```
研究主管 (research-lead)
├── 核心分析 (6 个)
│   ├── market-analyst 📊
│   ├── fundamental-analyst 💰
│   ├── technical-analyst 📈
│   ├── news-analyst 📰
│   ├── sentiment-analyst 😊
│   └── risk-analyst ⚠️
│
├── 研究团队 (4 个)
│   ├── researcher-1 🏭
│   ├── researcher-2 🏢
│   ├── economic-library 📚
│   └── research-lead 🔬
│
├── 交易决策 (4 个)
│   ├── trading-manager 🎯
│   ├── portfolio-manager 💼
│   ├── trader 💹
│   └── post-processor 📄
│
├── 新增能力 (4 个) 🆕
│   ├── bull-researcher 🐂
│   ├── bear-researcher 🐻
│   ├── timing-analyst ⏰
│   └── position-analyst 📊
│
└── 其他 (3 个)
    ├── dmgj_v1
    ├── main
    └── trade-executor ✅
```

**对比优势**:
- ✅ 更细的分工 (21 vs 6)
- ✅ 多空对比分析能力
- ✅ 时机和仓位专业能力
- ✅ 研究团队支持

---

## 🔧 可借鉴的技术点

### 1. 数据源适配器模式
```python
# 我们可以借鉴的架构
data_sources/
├── base.py (基础接口定义)
├── tushare_adapter.py
├── akshare_adapter.py
├── baostock_adapter.py
└── finnhub_adapter.py
```

**应用计划**:
- 创建统一的 data_source 工具
- 支持多个数据源切换
- 数据源故障自动降级

### 2. 分析服务分层
```python
services/
├── stock_data_service.py (数据服务)
├── analysis_service.py (分析服务)
├── report_service.py (报告服务)
└── sync_service.py (同步服务)
```

**应用计划**:
- 优化 Agent 间的服务调用
- 建立统一的数据缓存层
- 添加数据同步机制

### 3. API 路由设计
```python
routers/
├── stocks.py (股票数据)
├── analysis.py (分析任务)
├── reports.py (报告导出)
└── favorites.py (自选股)
```

**应用计划**:
- 当前通过 Agent 消息路由
- 可考虑添加 REST API 接口
- 支持外部系统集成

---

## 📈 系统优化方向

### 短期 (本周)
1. ✅ 学习 Tushare API 高级用法
2. ✅ 优化投资 6 大标准到分析模板
3. ⏭️ 集成 AKShare 数据源
4. ⏭️ 建立数据缓存机制

### 中期 (本月)
1. ⏭️ 创建统一数据源适配器
2. ⏭️ 优化 Agent 协作流程
3. ⏭️ 添加 REST API 接口
4. ⏭️ 建立学习进度追踪系统

### 长期 (季度)
1. ⏭️ 完整 TradingAgents-CN 源码学习
2. ⏭️ 建立投资框架 v1.0
3. ⏭️ 输出 20 份深度研究报告
4. ⏭️ 系统迭代到 v3.0

---

## 📝 学习心得

### 收获
1. **架构清晰**: TradingAgents-CN 的分层架构值得借鉴
2. **数据源丰富**: 可以集成更多免费数据源
3. **投资标准明确**: 6 大标准可量化可执行

### 改进
1. **数据源单一**: 当前主要依赖 Tushare，需增加 AKShare
2. **缓存机制**: 缺少数据缓存，重复调用 API
3. **API 接口**: 仅有消息接口，缺少 REST API

### 应用
1. 将投资 6 大标准整合到 fundamental-analyst 模板
2. 创建 data_source 工具类，支持多数据源
3. 建立数据缓存，减少 API 调用

---

**学习持续中...** 📚🔬

*最后更新：2026-03-18 19:00*
