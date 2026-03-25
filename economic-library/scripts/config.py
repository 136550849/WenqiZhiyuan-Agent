#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件管理
加载环境变量和配置项
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

# 加载 .env 文件
env_path = PROJECT_ROOT / ".env"
if env_path.exists():
    load_dotenv(env_path)

# Tushare 配置
TUSHARE_TOKEN = os.getenv('TUSHARE_TOKEN', '')
TUSHARE_BASE_URL = os.getenv('TUSHARE_BASE_URL', 'https://api.tushare.pro')

# Feishu 配置
FEISHU_WEBHOOK = os.getenv('FEISHU_WEBHOOK', '')
FEISHU_CHAT_ID = os.getenv('FEISHU_CHAT_ID', '')

# 目录配置
DATA_DIR = PROJECT_ROOT / "data"
REPORTS_DIR = PROJECT_ROOT / "reports"
ALERTS_DIR = PROJECT_ROOT / "alerts"
CACHE_DIR = PROJECT_ROOT / "data" / "cache"

# 确保目录存在
for dir_path in [DATA_DIR, REPORTS_DIR, ALERTS_DIR, CACHE_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# 缓存配置
CACHE_EXPIRY_HOURS = int(os.getenv('CACHE_EXPIRY_HOURS', '24'))

# 持仓配置
HOLDINGS_FILE = PROJECT_ROOT / "config" / "holdings.json"

def get_holdings():
    """获取持仓配置"""
    if HOLDINGS_FILE.exists():
        with open(HOLDINGS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"holdings": []}

def save_holdings(holdings):
    """保存持仓配置"""
    HOLDINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(HOLDINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(holdings, f, ensure_ascii=False, indent=2)
