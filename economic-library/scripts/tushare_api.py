#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tushare API 封装模块
提供常用的市场数据获取接口

文档：https://tushare.pro/document/2
"""

import requests
import json
from datetime import datetime, timedelta
from .config import TUSHARE_TOKEN, TUSHARE_BASE_URL, CACHE_DIR, CACHE_EXPIRY_HOURS
import os

class TushareAPI:
    """Tushare API 客户端"""
    
    def __init__(self, token=None):
        self.token = token or TUSHARE_TOKEN
        self.base_url = TUSHARE_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        })
    
    def _request(self, api_name, params=None):
        """发送 API 请求"""
        payload = {
            "api_name": api_name,
            "token": self.token,
            "params": params or {}
        }
        
        try:
            response = self.session.post(self.base_url, json=payload)
            response.raise_for_status()
            result = response.json()
            
            if result.get('code') != 0:
                raise Exception(f"Tushare API 错误：{result.get('msg')}")
            
            return result.get('data', {})
        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求失败：{e}")
    
    def get_daily_basic(self, ts_code=None, trade_date=None):
        """
        获取每日大盘指标
        
        参数:
            ts_code: 股票代码 (可选)
            trade_date: 交易日期 YYYYMMDD (可选，默认今日)
        
        返回:
            dict: 包含大盘指标数据
        """
        if trade_date is None:
            trade_date = datetime.now().strftime('%Y%m%d')
        
        params = {
            "trade_date": trade_date
        }
        
        if ts_code:
            params["ts_code"] = ts_code
        
        return self._request("daily_basic", params)
    
    def get_index_daily(self, ts_code=None, trade_date=None):
        """
        获取大盘指数日线行情
        
        参数:
            ts_code: 指数代码 (可选)
            trade_date: 交易日期 YYYYMMDD (可选)
        
        返回:
            dict: 指数行情数据
        """
        if trade_date is None:
            trade_date = datetime.now().strftime('%Y%m%d')
        
        params = {
            "trade_date": trade_date
        }
        
        if ts_code:
            params["ts_code"] = ts_code
        
        return self._request("index_daily", params)
    
    def get_market_summary(self, trade_date=None):
        """
        获取市场概况
        
        返回:
            dict: 包含涨跌家数、成交量等汇总数据
        """
        if trade_date is None:
            trade_date = datetime.now().strftime('%Y%m%d')
        
        params = {"trade_date": trade_date}
        return self._request("daily_basic", params)
    
    def get_stock_list(self):
        """
        获取股票列表
        
        返回:
            list: 股票列表
        """
        return self._request("stock_basic", {"fields": "ts_code,symbol,name,area,industry,list_date"})
    
    def get_realtime_quotes(self, ts_codes):
        """
        获取实时行情 (需要 Level-2 权限)
        
        参数:
            ts_codes: 股票代码列表
        
        返回:
            list: 实时行情数据
        """
        # 注意：实时行情需要付费权限
        # 这里使用日线数据作为替代
        trade_date = datetime.now().strftime('%Y%m%d')
        results = []
        
        for ts_code in ts_codes:
            try:
                params = {
                    "ts_code": ts_code,
                    "trade_date": trade_date
                }
                data = self._request("daily", params)
                if data.get('items'):
                    results.append(data['items'][0])
            except Exception as e:
                print(f"获取 {ts_code} 数据失败：{e}")
        
        return results

def get_market_data():
    """获取市场数据（便捷函数）"""
    api = TushareAPI()
    
    try:
        # 获取大盘指数
        indices = {
            "shanghai": {"code": "000001.SH", "name": "上证指数"},
            "shenzhen": {"code": "399001.SZ", "name": "深证成指"},
            "chinext": {"code": "399006.SZ", "name": "创业板指"}
        }
        
        result = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "indices": {},
            "summary": {}
        }
        
        for key, info in indices.items():
            try:
                data = api.get_index_daily(ts_code=info["code"])
                if data.get('items'):
                    item = data['items'][0]  # 最新数据
                    # 假设返回格式：[ts_code, trade_date, close, open, high, low, pre_close, change, pct_chg, vol, amount]
                    result["indices"][key] = {
                        "name": info["name"],
                        "close": float(item[2]) if len(item) > 2 else 0,
                        "open": float(item[3]) if len(item) > 3 else 0,
                        "high": float(item[4]) if len(item) > 4 else 0,
                        "low": float(item[5]) if len(item) > 5 else 0,
                        "change": float(item[7]) if len(item) > 7 else 0,
                        "change_pct": float(item[8]) if len(item) > 8 else 0,
                        "volume": float(item[9]) if len(item) > 9 else 0,
                        "amount": float(item[10]) if len(item) > 10 else 0
                    }
            except Exception as e:
                print(f"获取 {info['name']} 数据失败：{e}")
                result["indices"][key] = {
                    "name": info["name"],
                    "close": 0,
                    "change_pct": 0,
                    "error": str(e)
                }
        
        # 获取市场概况
        try:
            basic = api.get_daily_basic()
            if basic.get('items'):
                item = basic['items'][0]
                result["summary"] = {
                    "turnover_rate": item[4] if len(item) > 4 else 0,  # 换手率
                    "turnover_rate_f": item[5] if len(item) > 5 else 0,  # 换手率 (自由流通)
                    "volume_ratio": item[6] if len(item) > 6 else 0,  # 量比
                    "pe": item[7] if len(item) > 7 else 0,  # 市盈率
                    "pe_ttm": item[8] if len(item) > 8 else 0,  # 市盈率 (TTM)
                    "pb": item[9] if len(item) > 9 else 0,  # 市净率
                    "total_mv": item[10] if len(item) > 10 else 0,  # 总市值
                    "circ_mv": item[11] if len(item) > 11 else 0  # 流通市值
                }
        except Exception as e:
            print(f"获取市场概况失败：{e}")
        
        return result
    
    except Exception as e:
        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "error": str(e),
            "indices": {},
            "summary": {}
        }

if __name__ == "__main__":
    # 测试
    print("测试 Tushare API...")
    data = get_market_data()
    print(json.dumps(data, ensure_ascii=False, indent=2))
