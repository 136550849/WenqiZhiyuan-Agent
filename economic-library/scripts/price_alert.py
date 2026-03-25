#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
价格预警脚本
监控持仓股票价格，触发止损/止盈警报

使用方法:
    python scripts/price_alert.py

输出:
    alerts/price_alerts_YYYY-MM-DD.json
"""

import sys
import json
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from datetime import datetime
from config import get_holdings, ALERTS_DIR
from tushare_api import TushareAPI

# 预警配置
ALERT_CONFIG = {
    "stop_loss_pct": -7.0,  # 止损线 -7%
    "take_profit_pct": 20.0,  # 止盈线 +20%
    "warning_pct": -3.0  # 预警线 -3%
}

def check_price_alerts():
    """检查价格预警"""
    print("🔔 开始检查价格预警...")
    
    alerts = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "stop_loss": [],
        "take_profit": [],
        "warning": [],
        "watch": []
    }
    
    # 获取持仓
    holdings_data = get_holdings()
    holdings = holdings_data.get("holdings", [])
    
    if not holdings:
        print("⚠️ 暂无持仓配置")
        return alerts
    
    # 初始化 API
    api = TushareAPI()
    trade_date = datetime.now().strftime('%Y%m%d')
    
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
                profit_pct = ((current_price - cost_price) / cost_price) * 100
                profit_amount = (current_price - cost_price) * shares
                
                stock_info = {
                    "ts_code": ts_code,
                    "name": name,
                    "cost_price": cost_price,
                    "current_price": current_price,
                    "profit_pct": round(profit_pct, 2),
                    "profit_amount": round(profit_amount, 2),
                    "shares": shares
                }
                
                # 判断预警级别
                if profit_pct <= ALERT_CONFIG["stop_loss_pct"]:
                    alerts["stop_loss"].append(stock_info)
                elif profit_pct >= ALERT_CONFIG["take_profit_pct"]:
                    alerts["take_profit"].append(stock_info)
                elif profit_pct <= ALERT_CONFIG["warning_pct"]:
                    alerts["warning"].append(stock_info)
                else:
                    alerts["watch"].append(stock_info)
                    
        except Exception as e:
            print(f"获取 {ts_code} 价格失败：{e}")
            alerts["watch"].append({
                "ts_code": ts_code,
                "name": name,
                "error": str(e)
            })
    
    # 输出结果
    if not alerts["stop_loss"] and not alerts["take_profit"] and not alerts["warning"]:
        print("✅ 无预警触发")
    else:
        if alerts["stop_loss"]:
            print(f"🚨 止损警报：{len(alerts['stop_loss'])} 只股票")
            for s in alerts["stop_loss"]:
                print(f"   - {s['name']}: {s['profit_pct']}%")
        if alerts["take_profit"]:
            print(f"🎯 止盈警报：{len(alerts['take_profit'])} 只股票")
            for s in alerts["take_profit"]:
                print(f"   - {s['name']}: {s['profit_pct']}%")
        if alerts["warning"]:
            print(f"⚠️ 预警：{len(alerts['warning'])} 只股票")
            for s in alerts["warning"]:
                print(f"   - {s['name']}: {s['profit_pct']}%")
    
    return alerts

def save_alerts(alerts):
    """保存预警结果"""
    os.makedirs("alerts", exist_ok=True)
    filename = f"alerts/price_alerts_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(alerts, f, ensure_ascii=False, indent=2)
    
    return filename

def main():
    """主函数"""
    try:
        alerts = check_price_alerts()
        output_file = save_alerts(alerts)
        
        # 推送警报
        from feishu_push import send_alert_message
        
        has_urgent = False
        
        # 发送止损警报
        if alerts["stop_loss"]:
            send_alert_message("stop_loss", alerts["stop_loss"])
            has_urgent = True
        
        # 发送止盈警报
        if alerts["take_profit"]:
            send_alert_message("take_profit", alerts["take_profit"])
            has_urgent = True
        
        # 发送预警（可选）
        if alerts["warning"]:
            send_alert_message("warning", alerts["warning"])
        
        if has_urgent:
            print(f"⚠️ 已推送紧急警报")
            return 2
        else:
            print(f"✅ 价格预警检查完成：{output_file}")
            return 0
    except Exception as e:
        print(f"❌ 错误：{e}")
        return 1

if __name__ == "__main__":
    exit(main())
