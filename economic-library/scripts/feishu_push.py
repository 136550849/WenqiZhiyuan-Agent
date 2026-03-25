#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书消息推送模块
支持文本、Markdown、卡片消息推送

文档：https://open.feishu.cn/document/ukTMukTMukTM/ucTM5YjL3ETO24yNxkjN
"""

import requests
import json
from datetime import datetime
from .config import FEISHU_WEBHOOK, FEISHU_CHAT_ID

def send_text_message(content, webhook=None):
    """
    发送纯文本消息
    
    参数:
        content: 消息内容
        webhook: Webhook 地址 (可选，默认使用配置的)
    """
    webhook_url = webhook or FEISHU_WEBHOOK
    
    if not webhook_url:
        print("⚠️ 未配置飞书 Webhook")
        return False
    
    payload = {
        "msg_type": "text",
        "content": {
            "text": content
        }
    }
    
    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if result.get('code') == 0:
            print("✅ 消息发送成功")
            return True
        else:
            print(f"❌ 消息发送失败：{result}")
            return False
    except Exception as e:
        print(f"❌ 发送消息异常：{e}")
        return False

def send_markdown_message(content, webhook=None):
    """
    发送 Markdown 消息
    
    参数:
        content: Markdown 内容
        webhook: Webhook 地址
    """
    webhook_url = webhook or FEISHU_WEBHOOK
    
    if not webhook_url:
        print("⚠️ 未配置飞书 Webhook")
        return False
    
    payload = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": "📊 投资报告"
                },
                "template": "blue"
            },
            "elements": [
                {
                    "tag": "markdown",
                    "content": content
                }
            ]
        }
    }
    
    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if result.get('code') == 0:
            print("✅ Markdown 消息发送成功")
            return True
        else:
            print(f"❌ 消息发送失败：{result}")
            return False
    except Exception as e:
        print(f"❌ 发送消息异常：{e}")
        return False

def send_alert_message(alert_type, alerts, webhook=None):
    """
    发送预警消息
    
    参数:
        alert_type: 警报类型 (stop_loss/take_profit/warning)
        alerts: 警报列表
        webhook: Webhook 地址
    """
    webhook_url = webhook or FEISHU_WEBHOOK
    
    if not webhook_url:
        print("⚠️ 未配置飞书 Webhook")
        return False
    
    # 根据警报类型设置颜色和图标
    alert_config = {
        "stop_loss": {"color": "red", "icon": "🚨", "title": "止损警报"},
        "take_profit": {"color": "green", "icon": "🎯", "title": "止盈警报"},
        "warning": {"color": "orange", "icon": "⚠️", "title": "预警提示"}
    }
    
    config = alert_config.get(alert_type, {"color": "blue", "icon": "📢", "title": "通知"})
    
    # 构建消息内容
    stock_list = "\n".join([
        f"• **{s['name']}** ({s['ts_code']}): {s['profit_pct']}% (¥{s['profit_amount']})"
        for s in alerts
    ])
    
    payload = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": f"{config['icon']} {config['title']}"
                },
                "template": config["color"]
            },
            "elements": [
                {
                    "tag": "markdown",
                    "content": f"**触发时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n{stock_list}"
                },
                {
                    "tag": "note",
                    "elements": [
                        {
                            "tag": "plain_text",
                            "content": f"共 {len(alerts)} 只股票触发{config['title']}"
                        }
                    ]
                }
            ]
        }
    }
    
    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if result.get('code') == 0:
            print(f"✅ {config['title']} 发送成功")
            return True
        else:
            print(f"❌ 消息发送失败：{result}")
            return False
    except Exception as e:
        print(f"❌ 发送消息异常：{e}")
        return False

def send_portfolio_summary(summary, webhook=None):
    """
    发送持仓汇总消息
    
    参数:
        summary: 持仓汇总数据
        webhook: Webhook 地址
    """
    webhook_url = webhook or FEISHU_WEBHOOK
    
    if not webhook_url:
        print("⚠️ 未配置飞书 Webhook")
        return False
    
    # 计算涨跌颜色
    profit_pct = summary.get('profit_pct', 0)
    color = "green" if profit_pct >= 0 else "red"
    icon = "📈" if profit_pct >= 0 else "📉"
    
    # 构建消息内容
    holdings_text = "\n".join([
        f"• **{h['name']}**: {h['profit_pct']:+.2f}% (¥{h['profit']:,.2f})"
        for h in summary.get('holdings', [])[:5]  # 只显示前 5 只
    ])
    
    payload = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": f"{icon} 持仓监控日报"
                },
                "template": color
            },
            "elements": [
                {
                    "tag": "div",
                    "fields": [
                        {
                            "is_short": True,
                            "text": {
                                "tag": "lark_md",
                                "content": f"**总投入**\n¥{summary.get('total_invested', 0):,.2f}"
                            }
                        },
                        {
                            "is_short": True,
                            "text": {
                                "tag": "lark_md",
                                "content": f"**总市值**\n¥{summary.get('total_market_value', 0):,.2f}"
                            }
                        },
                        {
                            "is_short": True,
                            "text": {
                                "tag": "lark_md",
                                "content": f"**总盈亏**\n¥{summary.get('total_profit', 0):,.2f}"
                            }
                        },
                        {
                            "is_short": True,
                            "text": {
                                "tag": "lark_md",
                                "content": f"**收益率**\n{profit_pct:+.2f}%"
                            }
                        }
                    ]
                },
                {
                    "tag": "divider"
                },
                {
                    "tag": "markdown",
                    "content": f"**持仓明细** (前 5 只)\n{holdings_text}"
                },
                {
                    "tag": "note",
                    "elements": [
                        {
                            "tag": "plain_text",
                            "content": f"数据日期：{summary.get('date', '未知')} | 共 {len(summary.get('holdings', []))} 只股票"
                        }
                    ]
                }
            ]
        }
    }
    
    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if result.get('code') == 0:
            print("✅ 持仓汇总发送成功")
            return True
        else:
            print(f"❌ 消息发送失败：{result}")
            return False
    except Exception as e:
        print(f"❌ 发送消息异常：{e}")
        return False

if __name__ == "__main__":
    # 测试
    print("测试飞书消息推送...")
    
    # 测试文本消息
    send_text_message("这是一条测试消息")
    
    # 测试 Markdown 消息
    send_markdown_message("**测试** Markdown 消息\n- 项目 1\n- 项目 2")
