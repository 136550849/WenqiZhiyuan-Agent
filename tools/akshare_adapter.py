# 📊 AKShare 数据源适配器

**创建日期**: 2026-03-18  
**版本**: v1.0  
**用途**: 集成 AKShare 免费数据源，作为 Tushare 的补充和备份

---

## 📦 安装依赖

```bash
pip install akshare pandas
```

---

## 🔧 核心功能

### 1. 股票基础数据

```python
import akshare as ak
import pandas as pd

def get_stock_info(ts_code):
    """获取股票基本信息"""
    # 转换代码格式 (000001.SZ → 000001)
    code = ts_code.split('.')[0]
    
    # 获取个股信息
    df = ak.stock_individual_info_em(symbol=code)
    return df

def get_stock_price(ts_code, start_date, end_date):
    """获取股票行情数据"""
    code = ts_code.split('.')[0]
    df = ak.stock_zh_a_hist(
        symbol=code,
        period="daily",
        start_date=start_date.replace('-', ''),
        end_date=end_date.replace('-', ''),
        adjust="qfq"  # 前复权
    )
    return df
```

### 2. 财务数据

```python
def get_financial_metrics(ts_code):
    """获取财务指标"""
    code = ts_code.split('.')[0]
    
    # 获取财务指标
    df = ak.stock_financial_analysis_indicator(symbol=code)
    return df

def get_income_statement(ts_code):
    """获取利润表"""
    code = ts_code.split('.')[0]
    df = ak.stock_financial_report_sina(stock=code, symbol="利润表")
    return df

def get_balance_sheet(ts_code):
    """获取资产负债表"""
    code = ts_code.split('.')[0]
    df = ak.stock_financial_report_sina(stock=code, symbol="资产负债表")
    return df

def get_cash_flow(ts_code):
    """获取现金流量表"""
    code = ts_code.split('.')[0]
    df = ak.stock_financial_report_sina(stock=code, symbol="现金流量表")
    return df
```

### 3. 估值数据

```python
def get_valuation_data(ts_code):
    """获取估值数据"""
    code = ts_code.split('.')[0]
    
    # 获取市盈率、市净率等
    df = ak.stock_value_em(symbol=code)
    return df

def get_market_cap(ts_code):
    """获取市值数据"""
    code = ts_code.split('.')[0]
    df = ak.stock_individual_info_em(symbol=code)
    # 提取市值信息
    return df
```

### 4. 行业板块数据

```python
def get_sector_stocks(sector_name):
    """获取板块成分股"""
    df = ak.stock_board_industry_cons_em(symbol=sector_name)
    return df

def get_sector_performance(sector_name):
    """获取板块行情"""
    df = ak.stock_board_industry_name_em(symbol=sector_name)
    return df
```

### 5. 资金流向

```python
def get_north_flow(ts_code):
    """获取北向资金流向"""
    code = ts_code.split('.')[0]
    df = ak.stock_hsgt_north_net_flow_in_em(symbol=code)
    return df

def get_main_flow(ts_code):
    """获取主力资金流向"""
    code = ts_code.split('.')[0]
    df = ak.stock_main_force_net_flow_in_em(symbol=code)
    return df
```

---

## 🎯 投资 6 大标准筛选

```python
def screen_stocks_by_6standards():
    """
    根据投资 6 大标准筛选股票
    
    标准:
    1. 市值 > 100 亿
    2. ROE > 15%
    3. 营收增长率 > 20%
    4. 净利润增长率 > 20%
    5. 毛利率 > 30%
    6. 负债率 < 50%
    """
    
    # 获取全部 A 股列表
    all_stocks = ak.stock_info_a_code_name()
    
    qualified_stocks = []
    
    for _, row in all_stocks.iterrows():
        code = row['code']
        name = row['name']
        
        try:
            # 1. 市值筛选
            market_data = get_market_cap(code)
            total_mv = extract_market_cap(market_data)  # 单位：亿
            if total_mv < 100:
                continue
            
            # 2. ROE 筛选
            financial_data = get_financial_metrics(code)
            roe = extract_roe(financial_data)  # 单位：%
            if roe < 15:
                continue
            
            # 3-4. 成长性筛选
            revenue_growth = extract_revenue_growth(financial_data)
            net_profit_growth = extract_net_profit_growth(financial_data)
            if revenue_growth < 20 or net_profit_growth < 20:
                continue
            
            # 5. 毛利率筛选
            gross_margin = extract_gross_margin(financial_data)
            if gross_margin < 30:
                continue
            
            # 6. 负债率筛选
            debt_ratio = extract_debt_ratio(financial_data)
            if debt_ratio > 50:
                continue
            
            # 通过所有筛选
            qualified_stocks.append({
                'code': code,
                'name': name,
                'market_cap': total_mv,
                'roe': roe,
                'revenue_growth': revenue_growth,
                'net_profit_growth': net_profit_growth,
                'gross_margin': gross_margin,
                'debt_ratio': debt_ratio
            })
            
        except Exception as e:
            print(f"Error processing {code}: {e}")
            continue
    
    return pd.DataFrame(qualified_stocks)

def extract_market_cap(data):
    """提取市值 (亿)"""
    # 根据实际数据结构提取
    return float(data[data['item'] == '总市值']['value'].iloc[0]) / 100000000

def extract_roe(data):
    """提取 ROE (%)"""
    return float(data['加权净资产收益率 (%)'].iloc[0])

def extract_revenue_growth(data):
    """提取营收增长率 (%)"""
    return float(data['营业总收入同比增长率 (%)'].iloc[0])

def extract_net_profit_growth(data):
    """提取净利润增长率 (%)"""
    return float(data['归属母公司股东的净利润同比增长率 (%)'].iloc[0])

def extract_gross_margin(data):
    """提取毛利率 (%)"""
    return float(data['销售毛利率 (%)'].iloc[0])

def extract_debt_ratio(data):
    """提取负债率 (%)"""
    return float(data['资产负债率 (%)'].iloc[0])
```

---

## 📈 使用示例

```python
# 示例 1: 获取股票基本信息
stock_info = get_stock_info('000001.SZ')
print(stock_info)

# 示例 2: 获取历史行情
price_data = get_stock_price('000001.SZ', '2026-01-01', '2026-03-18')
print(price_data)

# 示例 3: 获取财务数据
financial_data = get_financial_metrics('000001.SZ')
print(financial_data)

# 示例 4: 筛选符合 6 大标准的股票
qualified = screen_stocks_by_6standards()
print(f"找到 {len(qualified)} 只符合条件的股票")
print(qualified.head())

# 示例 5: 获取北向资金流向
north_flow = get_north_flow('000001.SZ')
print(north_flow)
```

---

## ⚠️ 注意事项

1. **数据延迟**: AKShare 数据可能有 15 分钟延迟
2. **调用频率**: 避免高频调用，建议添加缓存
3. **数据验证**: 重要数据建议与 Tushare 交叉验证
4. **异常处理**: 网络请求可能失败，需要完善的异常处理

---

## 🔗 参考文档

- AKShare 官方文档：https://akshare.akfamily.xyz/
- GitHub: https://github.com/akfamily/akshare
- 数据源列表：https://akshare.akfamily.xyz/data.html

---

*版本：v1.0*  
*创建日期：2026-03-18*  
*作者：research-lead 🔬*
