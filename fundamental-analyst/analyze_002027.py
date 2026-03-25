import tushare as ts
import json
from datetime import datetime

# 初始化 Tushare
ts.set_token('eb0a4fb17ede71c5d34a3eca96758681b31af97f0ade9f0a3711e877')
pro = ts.pro_api()

def analyze_stock(ts_code):
    """完整股票分析"""
    result = {
        'ts_code': ts_code,
        'basic': {},
        'daily_basic': {},
        'fina_indicator': {},
        'income': [],
        'balance': [],
        'cashflow': [],
        'mainbiz': {}
    }
    
    # 1. 获取股票基本信息
    try:
        df = pro.stock_basic(fields='ts_code,symbol,name,area,industry,market,list_date,total_shares')
        stock = df[df['ts_code'] == ts_code]
        if not stock.empty:
            result['basic'] = stock.iloc[0].to_dict()
            print(f"[OK] 基本信息：{result['basic'].get('name', 'N/A')}")
    except Exception as e:
        print(f"[ERR] 基本信息失败：{e}")
    
    # 2. 获取每日基本面（PE、PB 等）
    try:
        df = pro.daily_basic(ts_code=ts_code, fields='ts_code,trade_date,pe,pe_ttm,pb,ps,total_mv,circ_mv,turnover_rate,dv_ratio')
        if not df.empty:
            result['daily_basic'] = df.iloc[0].to_dict()
            print(f"[OK] 估值指标：PE={result['daily_basic'].get('pe_ttm', 'N/A')}, PB={result['daily_basic'].get('pb', 'N/A')}")
    except Exception as e:
        print(f"[ERR] 估值指标失败：{e}")
    
    # 3. 获取财务指标（最新报告期）
    try:
        df = pro.fina_indicator(ts_code=ts_code)
        if not df.empty:
            result['fina_indicator'] = df.iloc[0].to_dict()
            print(f"[OK] 财务指标：ROE={result['fina_indicator'].get('roe', 'N/A')}%")
    except Exception as e:
        print(f"[ERR] 财务指标失败：{e}")
    
    # 4. 获取利润表
    try:
        df = pro.income(ts_code=ts_code, fields='ts_code,end_date,total_revenue,oper_revenue,oper_cost,oper_profit,net_profit', limit=5)
        if not df.empty:
            result['income'] = df.to_dict('records')
            print(f"[OK] 利润表：获取{len(result['income'])}期数据")
    except Exception as e:
        print(f"[ERR] 利润表失败：{e}")
    
    # 5. 获取资产负债表
    try:
        df = pro.balancesheet(ts_code=ts_code, fields='ts_code,end_date,total_assets,total_liab,total_hldr_eqy_inc_min_int,cash_equivalents', limit=5)
        if not df.empty:
            result['balance'] = df.to_dict('records')
            print(f"[OK] 资产负债表：获取{len(result['balance'])}期数据")
    except Exception as e:
        print(f"[ERR] 资产负债表失败：{e}")
    
    # 6. 获取现金流量表
    try:
        df = pro.cashflow(ts_code=ts_code, fields='ts_code,end_date,oper_cf,invest_cf,finan_cf', limit=5)
        if not df.empty:
            result['cashflow'] = df.to_dict('records')
            print(f"[OK] 现金流量表：获取{len(result['cashflow'])}期数据")
    except Exception as e:
        print(f"[ERR] 现金流量表失败：{e}")
    
    # 7. 获取主营业务
    try:
        df = pro.fina_mainbz(ts_code=ts_code, period='20241231')
        if not df.empty:
            result['mainbiz'] = df.to_dict('records')
            print(f"[OK] 主营业务：获取{len(result['mainbiz'])}条数据")
    except Exception as e:
        print(f"[ERR] 主营业务失败：{e}")
    
    return result

if __name__ == "__main__":
    ts_code = "002027.SZ"
    print(f"\n{'='*60}")
    print(f"股票基本面分析 - {ts_code}")
    print(f"分析时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    result = analyze_stock(ts_code)
    
    # 保存结果
    output_file = f"fundamental_data_{ts_code.replace('.', '_')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*60}")
    print(f"数据已保存到：{output_file}")
    print(f"{'='*60}\n")
    
    # 输出关键数据摘要
    print("【关键数据摘要】")
    if result['basic']:
        print(f"  公司名称：{result['basic'].get('name', 'N/A')}")
        print(f"  所属行业：{result['basic'].get('industry', 'N/A')}")
    
    if result['daily_basic']:
        print(f"  交易日期：{result['daily_basic'].get('trade_date', 'N/A')}")
        print(f"  市盈率 (TTM): {result['daily_basic'].get('pe_ttm', 'N/A')}")
        print(f"  市净率 (PB): {result['daily_basic'].get('pb', 'N/A')}")
        print(f"  总市值：{result['daily_basic'].get('total_mv', 'N/A')} 亿元")
    
    if result['fina_indicator']:
        print(f"  ROE: {result['fina_indicator'].get('roe', 'N/A')}%")
        print(f"  毛利率：{result['fina_indicator'].get('gross_margin', 'N/A')}%")
        print(f"  净利率：{result['fina_indicator'].get('net_profit_margin', 'N/A')}%")
        print(f"  资产负债率：{result['fina_indicator'].get('debt_to_assets', 'N/A')}%")
        print(f"  营收增长率：{result['fina_indicator'].get('op_yoy', 'N/A')}%")
        print(f"  净利润增长率：{result['fina_indicator'].get('dp_yoy', 'N/A')}%")
    
    print("\n")
