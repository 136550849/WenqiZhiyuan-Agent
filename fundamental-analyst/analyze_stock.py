import tushare as ts
import json
from datetime import datetime

# 初始化 Tushare (需要 token)
# Token 配置：2026-03-21 更新
try:
    ts.set_token('eb0a4fb17ede71c5d34a3eca96758681b31af97f0ade9f0a3711e877')
    pro = ts.pro_api()
except Exception as e:
    print(f"Tushare 初始化失败：{e}")
    pro = None

def get_stock_basic_info(ts_code):
    """获取股票基本信息"""
    try:
        if pro:
            df = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,market,list_date')
            stock = df[df['ts_code'] == ts_code]
            if not stock.empty:
                return stock.iloc[0].to_dict()
    except Exception as e:
        print(f"获取基本信息失败：{e}")
    return None

def get_financial_indicators(ts_code):
    """获取财务指标"""
    try:
        if pro:
            # 获取主要财务指标
            df = pro.fina_indicator(ts_code=ts_code)
            if not df.empty:
                return df.iloc[0].to_dict()
    except Exception as e:
        print(f"获取财务指标失败：{e}")
    return None

def get_income_statement(ts_code):
    """获取利润表"""
    try:
        if pro:
            df = pro.income(ts_code=ts_code, fields='ts_code,end_date,total_revenue,operating_profit,net_profit')
            if not df.empty:
                return df.head(5).to_dict('records')
    except Exception as e:
        print(f"获取利润表失败：{e}")
    return None

def get_balance_sheet(ts_code):
    """获取资产负债表"""
    try:
        if pro:
            df = pro.balancesheet(ts_code=ts_code, fields='ts_code,end_date,total_assets,total_liq,total_hldr_eqy_inc_min_int')
            if not df.empty:
                return df.head(5).to_dict('records')
    except Exception as e:
        print(f"获取资产负债表失败：{e}")
    return None

def get_cash_flow(ts_code):
    """获取现金流量表"""
    try:
        if pro:
            df = pro.cashflow(ts_code=ts_code, fields='ts_code,end_date,oper_cf,invest_cf,finan_cf')
            if not df.empty:
                return df.head(5).to_dict('records')
    except Exception as e:
        print(f"获取现金流量表失败：{e}")
    return None

def get_daily_basic(ts_code):
    """获取每日基本面数据（PE、PB 等）"""
    try:
        if pro:
            # 获取最近交易日数据
            df = pro.daily_basic(ts_code=ts_code, trade_date='', fields='ts_code,trade_date,pe,pe_ttm,pb,ps,total_mv,circ_mv')
            if not df.empty:
                return df.iloc[0].to_dict()
    except Exception as e:
        print(f"获取每日基本面失败：{e}")
    return None

if __name__ == "__main__":
    # 分析贵州茅台
    ts_code = "600519.SH"
    print(f"\n{'='*60}")
    print(f"股票基本面分析 - {ts_code}")
    print(f"{'='*60}\n")
    
    # 获取基本信息
    basic = get_stock_basic_info(ts_code)
    if basic:
        print("【基本信息】")
        print(f"  股票代码：{basic.get('ts_code', 'N/A')}")
        print(f"  股票简称：{basic.get('name', 'N/A')}")
        print(f"  所属行业：{basic.get('industry', 'N/A')}")
        print(f"  上市日期：{basic.get('list_date', 'N/A')}")
        print()
    
    # 获取估值指标
    daily_basic = get_daily_basic(ts_code)
    if daily_basic:
        print("【估值指标】")
        print(f"  市盈率 (PE): {daily_basic.get('pe', 'N/A')}")
        print(f"  市盈率 (TTM): {daily_basic.get('pe_ttm', 'N/A')}")
        print(f"  市净率 (PB): {daily_basic.get('pb', 'N/A')}")
        print(f"  总市值：{daily_basic.get('total_mv', 'N/A')} 亿元")
        print(f"  流通市值：{daily_basic.get('circ_mv', 'N/A')} 亿元")
        print()
    
    # 获取财务指标
    fina = get_financial_indicators(ts_code)
    if fina:
        print("【核心财务指标】")
        print(f"  ROE (净资产收益率): {fina.get('roe', 'N/A')}%")
        print(f"  毛利率: {fina.get('gross_margin', 'N/A')}%")
        print(f"  净利率: {fina.get('net_profit_margin', 'N/A')}%")
        print(f"  资产负债率: {fina.get('debt_to_assets', 'N/A')}%")
        print()
    
    print("\n分析完成！")
