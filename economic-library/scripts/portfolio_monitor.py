#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
持仓监控日报脚本
生成持仓盈亏汇总报告

使用方法:
    python scripts/portfolio_monitor.py

输出:
    reports/portfolio_YYYY-MM-DD.json
"""

import sys
import json
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from datetime import datetime
from config import get_holdings, REPORTS_DIR
from tushare_api import TushareAPI

def get_portfolio_summary():
    """获取持仓汇总"""
    print("📊 开始生成持仓监控日报...")
    
    # 获取持仓
    holdings_data = get_holdings()
    holdings = holdings_data.get("holdings", [])
    
    if not holdings:
        print("⚠️ 暂无持仓配置")
        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "total_invested": 0,
            "total_market_value": 0,
            "total_profit": 0,
            "profit_pct": 0,
            "top_gainers": [],
            "top_losers": [],
            "holdings": [],
            "note": "暂无持仓配置"
        }
    
    # 初始化 API
    api = TushareAPI()
    trade_date = datetime.now().strftime('%Y%m%d')
    
    summary = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "total_invested": 0,
        "total_market_value": 0,
        "total_profit": 0,
        "profit_pct": 0,
        "top_gainers": [],
        "top_losers": [],
        "holdings": []
    }
    
    # 获取持仓股票最新价格
    for holding in holdings:
        ts_code = holding.get("ts_code")
        name = holding.get("name", ts_code)
        cost_price = holding.get("cost_price", 0)
        shares = holding.get("shares", 0)
        
        if not ts_code or not cost_price:
            continue
        
        try:
            # 获取日线数据
            data = api.get_index_daily(ts_code=ts_code, trade_date=trade_date)
            
            if data.get('items'):
                item = data['items'][0]
                current_price = float(item[2]) if len(item) > 2 else 0
                
                # 计算盈亏
                invested = cost_price * shares
                market_value = current_price * shares
                profit = market_value - invested
                profit_pct = (profit / invested) * 100 if invested > 0 else 0
                
                holding_info = {
                    "ts_code": ts_code,
                    "name": name,
                    "shares": shares,
                    "cost_price": cost_price,
                    "current_price": current_price,
                    "invested": round(invested, 2),
                    "market_value": round(market_value, 2),
                    "profit": round(profit, 2),
                    "profit_pct": round(profit_pct, 2)
                }
                
                summary["holdings"].append(holding_info)
                summary["total_invested"] += invested
                summary["total_market_value"] += market_value
                summary["total_profit"] += profit
                
        except Exception as e:
            print(f"获取 {ts_code} 数据失败：{e}")
            summary["holdings"].append({
                "ts_code": ts_code,
                "name": name,
                "error": str(e)
            })
    
    # 计算总盈亏比例
    if summary["total_invested"] > 0:
        summary["profit_pct"] = round((summary["total_profit"] / summary["total_invested"]) * 100, 2)
    
    # 排序找出涨跌 TOP3
    valid_holdings = [h for h in summary["holdings"] if "error" not in h]
    valid_holdings.sort(key=lambda x: x.get("profit_pct", 0), reverse=True)
    
    summary["top_gainers"] = valid_holdings[:3]
    summary["top_losers"] = valid_holdings[-3:] if len(valid_holdings) >= 3 else []
    
    # 四舍五入汇总数据
    summary["total_invested"] = round(summary["total_invested"], 2)
    summary["total_market_value"] = round(summary["total_market_value"], 2)
    summary["total_profit"] = round(summary["total_profit"], 2)
    
    return summary

def generate_report(summary):
    """生成持仓报告"""
    report = {
        "summary": summary,
        "analysis": {
            "market_value_change": summary["total_profit"],
            "change_pct": summary["profit_pct"],
            "recommendation": "功能待实现"
        }
    }
    return report

def save_report(report):
    """保存报告"""
    filename = REPORTS_DIR / f"portfolio_{datetime.now().strftime('%Y-%m-%d')}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 持仓报告已保存到 {filename}")
    return str(filename)

def main():
    """主函数"""
    try:
        summary = get_portfolio_summary()
        report = generate_report(summary)
        output_file = save_report(report)
        
        # 推送到飞书
        from feishu_push import send_portfolio_summary
        send_portfolio_summary(summary)
        
        print(f"✅ 持仓监控日报完成：{output_file}")
        return 0
    except Exception as e:
        print(f"❌ 错误：{e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())
