"""
风险分析师配置管理模块
Configuration Manager for Risk Analyst
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

class Config:
    """配置管理类"""
    
    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "settings.json"
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self._default_config()
    
    def _default_config(self) -> Dict[str, Any]:
        """默认配置"""
        return {
            "data_sources": {
                "stock_api": {
                    "enabled": False,
                    "provider": "",  # e.g., "tushare", "akshare", "yfinance"
                    "api_key": "",
                    "endpoint": ""
                },
                "financial_data": {
                    "enabled": False,
                    "provider": "",
                    "api_key": ""
                },
                "macro_data": {
                    "enabled": False,
                    "provider": "",
                    "api_key": ""
                }
            },
            "risk_thresholds": {
                "high_risk": 70,      # ≥70 高风险
                "medium_high_risk": 50,  # 50-69 中高风险
                "medium_risk": 30,    # 30-49 中等风险
                "low_risk": 0         # <30 低风险
            },
            "position_limits": {
                "single_stock_max": 0.30,    # 单只股票上限 30%
                "single_industry_max": 0.50, # 单一行业上限 50%
                "max_total_position": 0.80   # 最大总仓位 80%
            },
            "stop_loss": {
                "fixed_ratios": [-0.05, -0.08, -0.10],  # 固定比例止损
                "time_limit_days": 10,  # 时间止损天数
                "trailing_stop_pct": 0.05  # 移动止损回撤比例
            }
        }
    
    def save(self):
        """保存配置"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def set(self, key: str, value: Any):
        """设置配置值"""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
    
    def is_data_source_configured(self, source: str) -> bool:
        """检查数据源是否已配置"""
        return self.get(f"data_sources.{source}.enabled", False)
    
    def check_all_data_sources(self) -> Dict[str, bool]:
        """检查所有数据源配置状态"""
        sources = self.config.get("data_sources", {})
        return {name: config.get("enabled", False) for name, config in sources.items()}


# 快捷访问
config = Config()

if __name__ == "__main__":
    # 测试配置
    print("=== 风险分析师配置检查 ===")
    print(f"\n数据源配置状态:")
    for source, enabled in config.check_all_data_sources().items():
        status = "[OK] 已配置" if enabled else "[--] 未配置"
        print(f"  {source}: {status}")
    
    print(f"\n风险阈值:")
    print(f"  高风险线：≥{config.get('risk_thresholds.high_risk')}")
    print(f"  中高风险线：{config.get('risk_thresholds.medium_high_risk')}-{config.get('risk_thresholds.high_risk')-1}")
    print(f"  中等风险线：{config.get('risk_thresholds.medium_risk')}-{config.get('risk_thresholds.medium_high_risk')-1}")
    print(f"  低风险线：< {config.get('risk_thresholds.medium_risk')}")
    
    print(f"\n仓位限制:")
    print(f"  单只股票上限：{config.get('position_limits.single_stock_max')*100}%")
    print(f"  单一行业上限：{config.get('position_limits.single_industry_max')*100}%")
    print(f"  最大总仓位：{config.get('position_limits.max_total_position')*100}%")
