#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
投资日报生成脚本
基于 Tushare 数据生成结构化投资日报

使用方法:
    python scripts/generate_daily_report.py

输出:
    reports/daily_report_YYYY-MM-DD.md
"""

import json
import os
from datetime import datetime

def load_market_data():
    """加载市场数据"""
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"data/tushare_daily_{today}.json"
    
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        print(f"⚠️ 未找到今日数据文件：{filename}")
        return None

def generate_report(data):
    """生成投资日报"""
    if not data:
        return "# 投资日报\n\n⚠️ 数据获取失败，请稍后重试。"
    
    report = f"""# 📊 投资日报

**日期**: {data.get('date', '未知')}

---

## 📈 大盘表现

| 指数 | 收盘价 | 涨跌幅 |
|------|--------|--------|
| 上证指数 | {data.get('indices', {}).get('shanghai', {}).get('close', 'N/A')} | {data.get('indices', {}).get('shanghai', {}).get('change_pct', 'N/A')}% |
| 深证成指 | {data.get('indices', {}).get('shenzhen', {}).get('close', 'N/A')} | {data.get('indices', {}).get('shenzhen', {}).get('change_pct', 'N/A')}% |
| 创业板指 | {data.get('indices', {}).get('chinext', {}).get('close', 'N/A')} | {data.get('indices', {}).get('chinext', {}).get('change_pct', 'N/A')}% |

---

## 📝 市场摘要

{data.get('summary', '暂无摘要')}

---

## 🔍 重点关注

- [ ] 待添加重点关注股票
- [ ] 待添加行业分析

---

## 💡 操作建议

*基于当前市场情况的建议*

---

*报告生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M")}*
"""
    return report

def save_report(report):
    """保存报告"""
    os.makedirs("reports", exist_ok=True)
    filename = f"reports/daily_report_{datetime.now().strftime('%Y-%m-%d')}.md"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ 日报已保存到 {filename}")
    return filename

def main():
    """主函数"""
    try:
        data = load_market_data()
        report = generate_report(data)
        output_file = save_report(report)
        print(f"✅ 投资日报生成完成：{output_file}")
        return 0
    except Exception as e:
        print(f"❌ 错误：{e}")
        return 1

if __name__ == "__main__":
    exit(main())
