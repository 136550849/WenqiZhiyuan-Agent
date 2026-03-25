# 📚 TradingAgents-CN 核心文档学习总结

**学习时间：** 2026-03-18 19:10-19:30  
**学习人：** 研研 📊  
**文档来源：** D:\BaiduNetdisk\LocalBackup\08-Courses\F-TradingAgents-CN

---

## 📖 已学习文档（3/13）

| 序号 | 文档 | 大小 | 状态 | 核心收获 |
|------|------|------|------|----------|
| 1 | README.md | 9.3KB | ✅ | 项目概览、快速开始 |
| 2 | 01-平台架构与开发指南.md | 15.1KB | ✅ | 技术架构、数据流转 |
| 3 | 07-Tushare 股票筛选使用指南.md | 7.8KB | ✅ | API 配置、6 大筛选条件 |

---

## 📊 文档 1: README.md 核心收获

### 项目信息
- **位置：** F:\TradingAgents-CN
- **用途：** 多智能体股票分析系统（开发者测试版）
- **目标用户：** 有 Python 基础，能独立排查问题的测试者

### 项目结构
```
F:\TradingAgents-CN\
├── 📘 文档中心
├── 🛠️ 脚本工具 (test_data_sources.py)
├── 📦 核心代码 (app/, tradingagents/, web/)
├── ⚙️ 配置文件 (.env, requirements.txt)
└── 📊 数据目录 (data/, cache/, results/, logs/)
```

### 快速开始 4 步骤
1. **安装依赖** - conda 创建虚拟环境，pip install
2. **配置环境变量** - 复制.env.example 并编辑
3. **运行测试** - 测试数据源、检查配置
4. **启动服务** - API 服务 (8000) + Web 界面 (8501)

### 数据源支持
| 数据源 | 类型 | 地区 | 密钥 | 推荐度 |
|--------|------|------|------|--------|
| AKShare | 股票/期货/基金 | A 股/港股/美股 | ❌ 免费 | ⭐⭐⭐⭐⭐ |
| Tushare | 股票/期货/基金 | A 股/港股/美股 | ✅ 需积分 | ⭐⭐⭐⭐ |
| BaoStock | 股票 | A 股 | ❌ 免费 | ⭐⭐⭐⭐ |
| Finnhub | 股票/外汇 | 美股/全球 | ✅ 需 API Key | ⭐⭐⭐ |

### AI 模型支持
| 模型 | 厂商 | 推荐度 | 说明 |
|------|------|--------|------|
| DeepSeek V3 | 深度求索 | ⭐⭐⭐⭐⭐ | 性价比最高 |
| 通义千问 | 阿里百炼 | ⭐⭐⭐⭐⭐ | 国产稳定 |
| GPT-4 | OpenAI | ⭐⭐⭐⭐ | 需要代理 |
| Gemini | Google | ⭐⭐⭐⭐ | 免费额度大 |
| Claude | Anthropic | ⭐⭐⭐⭐ | 长文本强 |

---

## 🏗️ 文档 2: 平台架构与开发指南 核心收获

### 技术架构
```
┌─────────────────────────────────────┐
│     前端 (Vue.js + Element Plus)    │
│     http://localhost:9981           │
└─────────────┬───────────────────────┘
              │ HTTP/REST + WebSocket
┌─────────────▼───────────────────────┐
│     后端 (FastAPI + Worker)         │
│     端口 8000 / 8001                 │
└─────────────┬───────────────────────┘
              │
    ┌─────────┼─────────┐
    │         │         │
┌───▼───┐ ┌──▼───┐ ┌──▼────┐
│MongoDB│ │Redis │ │文件存储│
└───────┘ └──────┘ └───────┘
```

### 后端目录结构详解
| 目录 | 说明 | 核心文件 |
|------|------|----------|
| app/ | FastAPI 应用 | main.py, worker.py |
| routers/ | API 路由 | stocks.py, analysis.py, favorites.py |
| services/ | 业务逻辑 | stock_data_service.py, analysis_service.py |
| models/ | 数据库模型 | stock.py, analysis.py |
| schemas/ | 数据验证 | Pydantic Schema |
| core/ | 核心配置 | config.py, database.py, security.py |
| middleware/ | 中间件 | auth.py, cors.py |
| utils/ | 工具函数 | logger.py, date_utils.py |

### 数据流转流程

#### 股票数据同步流程
```
用户点击"同步" → 前端发送 API → 后端接收 → 调用服务层
→ 选择数据源 → 调用 adapter → 访问外部 API → 获取数据
→ 存储 MongoDB → 返回结果 → 前端显示成功
```

#### AI 分析任务流程
```
用户点击"分析" → 创建分析任务 → 存入 MongoDB
→ Worker 轮询任务 → 调用 AI 模型 → 生成报告
→ 存储报告 → 更新任务状态 → 前端轮询显示结果
```

### 核心 API 接口
| 接口 | 方法 | 说明 |
|------|------|------|
| POST /api/favorites/{code}/sync | 同步股票数据 |
| POST /api/analysis/single | 单股分析 |
| POST /api/analysis/batch | 批量分析 |
| GET /api/stocks/{code} | 获取股票数据 |
| GET /api/reports/{id} | 获取分析报告 |

---

## 📈 文档 3: Tushare 股票筛选使用指南 核心收获

### Tushare API 配置
```python
import tushare as ts

# 配置 Token
TOKEN = 'eb0a4fb17ede71c5d34a3eca96758681b31af97f0ade9f0a3711e877'
pro = ts.pro_api(TOKEN)
```

### 6 大投资筛选条件

| 序号 | 条件 | 标准 | 数据来源 |
|------|------|------|----------|
| 1 | 市值 | > 100 亿 | daily_basic.total_mv |
| 2 | ROE | > 15% | fina_indicator.roe |
| 3 | 营收增长率 | > 20% | income.total_revenue 计算 |
| 4 | 净利润增长率 | > 20% | income.n_income_attr_p 计算 |
| 5 | 毛利率 | > 30% | income 计算 |
| 6 | 负债率 | < 50% | balancesheet 计算 |

### 核心计算公式
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

### 关键数据表
| 表名 | 说明 | 核心字段 |
|------|------|----------|
| daily_basic | 每日指标 | ts_code, total_mv, pe_ttm, pb |
| fina_indicator | 财务指标 | ts_code, roe, roa |
| income | 利润表 | total_revenue, n_income_attr_p |
| balancesheet | 资产负债表 | total_assets, total_liab |

---

## 🎯 学习收获总结

### 1. 系统架构理解
- **前端：** Vue.js + Element Plus (9981 端口)
- **后端：** FastAPI + Worker (8000/8001 端口)
- **数据库：** MongoDB (数据存储) + Redis (缓存)
- **数据源：** AKShare/Tushare/BaoStock/Finnhub
- **AI 模型：** DeepSeek/通义千问/GPT-4 等

### 2. 数据流转理解
- 股票同步：用户触发 → API → 数据源 → MongoDB
- AI 分析：任务创建 → Worker 轮询 → AI 模型 → 报告存储

### 3. 投资筛选标准
- 6 大条件：市值、ROE、营收增长、净利润增长、毛利率、负债率
- 数据来源：Tushare Pro API
- 计算方法：标准化公式

### 4. 配置要点
- 环境变量：.env 文件配置 MongoDB/Redis/API Keys
- 虚拟环境：conda 创建 tradingagents 环境
- 依赖安装：pip install -e . 或 requirements.txt

---

## 📋 待学习文档（10/13）

| 序号 | 文档 | 优先级 | 说明 |
|------|------|--------|------|
| 4 | 03-系统部署与优化指南.md | ⭐⭐⭐ | 部署配置 |
| 5 | 04-QMT 数据源对接配置指南.md | ⭐⭐ | QMT 配置 |
| 6 | 05-Python 学习速查手册.md | ⭐⭐⭐ | Python 基础 |
| 7 | 06-OpenClaw 配置与自动化指南.md | ⭐⭐⭐ | OpenClaw 集成 |
| 8 | 快速参考卡.md | ⭐⭐ | 速查表 |
| 9 | 测试报告模板.md | ⭐ | 测试用 |
| 10 | 00-投资者笔记整理.md | ⭐⭐⭐ | 投资笔记 |
| 11 | 其他文档 | ⭐⭐ | 补充学习 |

---

## 🚀 下一步行动

### 今日计划
- [ ] 学习 03-系统部署与优化指南.md
- [ ] 学习 06-OpenClaw 配置与自动化指南.md
- [ ] 输出优化日志

### 本周计划
- [ ] 完成剩余 10 个文档学习
- [ ] 配置 Tushare API（已有 Token）
- [ ] 测试 AKShare 数据源（免费）
- [ ] 建立行业筛选策略

### 本月计划
- [ ] 搭建 TradingAgents-CN 环境
- [ ] 实现 6 大条件股票筛选
- [ ] 输出第一份 AI 分析报告
- [ ] 建立行业跟踪清单

---

*学习时间：2026-03-18 19:10-19:30 | 版本：v2.1*
