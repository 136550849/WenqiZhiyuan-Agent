"""
止损止盈计算器
Stop-Loss and Take-Profit Calculator
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class StopLossType(Enum):
    """止损类型"""
    FIXED_PERCENT = "固定比例止损"
    TECHNICAL = "技术位止损"
    TIME = "时间止损"
    TRAILING = "移动止损"

@dataclass
class StopLossResult:
    """止损计算结果"""
    stop_type: StopLossType
    stop_price: float
    stop_percent: float
    loss_amount: float
    shares: int
    notes: str

@dataclass
class TakeProfitResult:
    """止盈计算结果"""
    target_price: float
    target_percent: float
    profit_amount: float
    shares: int
    notes: str

class StopLossCalculator:
    """止损计算器"""
    
    def __init__(self):
        # 默认止损比例
        self.fixed_ratios = [-0.05, -0.08, -0.10]  # -5%, -8%, -10%
        self.time_limit_days = 10
        self.trailing_stop_pct = 0.05  # 5% 回撤
    
    def calculate_fixed_stop(self,
                            entry_price: float,
                            shares: int,
                            stop_ratio: float = -0.08) -> StopLossResult:
        """
        计算固定比例止损
        
        Args:
            entry_price: 入场价格
            shares: 股数
            stop_ratio: 止损比例 (负数)
        
        Returns:
            StopLossResult: 止损结果
        """
        stop_price = entry_price * (1 + stop_ratio)
        loss_per_share = entry_price - stop_price
        loss_amount = loss_per_share * shares
        
        return StopLossResult(
            stop_type=StopLossType.FIXED_PERCENT,
            stop_price=round(stop_price, 2),
            stop_percent=abs(stop_ratio) * 100,
            loss_amount=loss_amount,
            shares=shares,
            notes=f"固定比例止损：下跌{abs(stop_ratio)*100:.0f}% 触发"
        )
    
    def calculate_technical_stop(self,
                                entry_price: float,
                                shares: int,
                                support_price: float) -> StopLossResult:
        """
        计算技术位止损
        
        Args:
            entry_price: 入场价格
            shares: 股数
            support_price: 支撑位价格
        
        Returns:
            StopLossResult: 止损结果
        """
        stop_percent = (support_price - entry_price) / entry_price
        loss_per_share = entry_price - support_price
        loss_amount = loss_per_share * shares
        
        return StopLossResult(
            stop_type=StopLossType.TECHNICAL,
            stop_price=support_price,
            stop_percent=abs(stop_percent) * 100,
            loss_amount=loss_amount,
            shares=shares,
            notes=f"技术位止损：跌破支撑位 {support_price} 触发"
        )
    
    def calculate_time_stop(self,
                           entry_price: float,
                           shares: int,
                           entry_date: str,
                           limit_days: int = 10) -> dict:
        """
        计算时间止损
        
        Args:
            entry_price: 入场价格
            shares: 股数
            entry_date: 入场日期 (YYYY-MM-DD)
            limit_days: 时间限制天数
        
        Returns:
            dict: 时间止损信息
        """
        from datetime import datetime, timedelta
        
        entry = datetime.strptime(entry_date, "%Y-%m-%d")
        deadline = entry + timedelta(days=limit_days)
        
        return {
            "stop_type": StopLossType.TIME,
            "entry_date": entry_date,
            "deadline": deadline.strftime("%Y-%m-%d"),
            "limit_days": limit_days,
            "notes": f"时间止损：{limit_days} 日内无表现则离场"
        }
    
    def calculate_trailing_stop(self,
                               entry_price: float,
                               shares: int,
                               current_price: float,
                               trailing_pct: float = 0.05) -> StopLossResult:
        """
        计算移动止损
        
        Args:
            entry_price: 入场价格
            shares: 股数
            current_price: 当前价格
            trailing_pct: 回撤比例
        
        Returns:
            StopLossResult: 止损结果
        """
        # 移动止损基于最高价
        highest_price = max(entry_price, current_price)
        stop_price = highest_price * (1 - trailing_pct)
        
        # 确保止损价不低于入场价（保护本金）
        if current_price > entry_price:
            stop_price = max(stop_price, entry_price * 1.02)  # 至少保护 2% 利润
        
        loss_per_share = max(0, entry_price - stop_price)
        loss_amount = loss_per_share * shares
        
        profit_per_share = max(0, current_price - entry_price)
        profit_amount = profit_per_share * shares
        
        return StopLossResult(
            stop_type=StopLossType.TRAILING,
            stop_price=round(stop_price, 2),
            stop_percent=trailing_pct * 100,
            loss_amount=loss_amount,
            shares=shares,
            notes=f"移动止损：从最高价回撤{trailing_pct*100:.0f}% 触发 | 当前浮盈：¥{profit_amount:,.0f}"
        )
    
    def recommend_stop_type(self,
                           risk_level: str,
                           volatility: str = "normal",
                           trading_style: str = "swing") -> StopLossType:
        """
        推荐止损类型
        
        Args:
            risk_level: 风险等级
            volatility: 波动率 ("low", "normal", "high")
            trading_style: 交易风格 ("day", "swing", "position")
        
        Returns:
            StopLossType: 推荐的止损类型
        """
        # 高风险或高波动：用较紧的固定止损
        if risk_level in ["high", "medium_high"] or volatility == "high":
            return StopLossType.FIXED_PERCENT
        
        # 日线交易：用技术位止损
        if trading_style == "day":
            return StopLossType.TECHNICAL
        
        # 趋势行情：用移动止损
        if trading_style == "position":
            return StopLossType.TRAILING
        
        # 默认：摆动交易用固定止损
        return StopLossType.FIXED_PERCENT
    
    def get_recommended_ratio(self, risk_level: str) -> float:
        """根据风险等级推荐止损比例"""
        ratios = {
            "high": -0.05,      # 高风险：-5% 紧止损
            "medium_high": -0.05,
            "medium": -0.08,    # 中等风险：-8% 标准止损
            "low": -0.10,       # 低风险：-10% 宽松止损
            "very_low": -0.12   # 极低风险：-12% 很宽松
        }
        return ratios.get(risk_level, -0.08)


class TakeProfitCalculator:
    """止盈计算器"""
    
    def __init__(self):
        # 默认止盈目标
        self.targets = [0.10, 0.20, 0.30]  # 10%, 20%, 30%
    
    def calculate_target_profit(self,
                               entry_price: float,
                               shares: int,
                               target_ratio: float = 0.20) -> TakeProfitResult:
        """
        计算目标价位止盈
        
        Args:
            entry_price: 入场价格
            shares: 股数
            target_ratio: 目标收益率
        
        Returns:
            TakeProfitResult: 止盈结果
        """
        target_price = entry_price * (1 + target_ratio)
        profit_per_share = target_price - entry_price
        profit_amount = profit_per_share * shares
        
        return TakeProfitResult(
            target_price=round(target_price, 2),
            target_percent=target_ratio * 100,
            profit_amount=profit_amount,
            shares=shares,
            notes=f"目标止盈：上涨{target_ratio*100:.0f}% 达到 {target_price:.2f}"
        )
    
    def calculate_batch_exit(self,
                            entry_price: float,
                            shares: int,
                            targets: List[float] = None) -> List[TakeProfitResult]:
        """
        计算分批止盈方案
        
        Args:
            entry_price: 入场价格
            shares: 股数
            targets: 目标收益率列表
        
        Returns:
            List[TakeProfitResult]: 止盈结果列表
        """
        if targets is None:
            targets = [0.15, 0.25, 0.35]  # 默认三批：15%, 25%, 35%
        
        results = []
        batch_shares = shares // len(targets)
        remaining = shares
        
        for i, target in enumerate(targets):
            if i == len(targets) - 1:
                # 最后一批用剩余全部
                current_shares = remaining
            else:
                current_shares = batch_shares
                remaining -= batch_shares
            
            result = self.calculate_target_profit(entry_price, current_shares, target)
            results.append(result)
        
        return results
    
    def calculate_trailing_profit(self,
                                  entry_price: float,
                                  shares: int,
                                  current_price: float,
                                  trailing_pct: float = 0.05) -> dict:
        """
        计算移动止盈
        
        Args:
            entry_price: 入场价格
            shares: 股数
            current_price: 当前价格
            trailing_pct: 回撤比例
        
        Returns:
            dict: 移动止盈信息
        """
        highest_price = max(entry_price, current_price)
        trigger_price = highest_price * (1 - trailing_pct)
        
        current_profit = (current_price - entry_price) * shares
        protected_profit = max(0, (trigger_price - entry_price) * shares)
        
        return {
            "highest_price": highest_price,
            "trigger_price": round(trigger_price, 2),
            "trailing_percent": trailing_pct * 100,
            "current_profit": current_profit,
            "protected_profit": protected_profit,
            "notes": f"移动止盈：从最高价回撤{trailing_pct*100:.0f}% 触发，已保护利润 ¥{protected_profit:,.0f}"
        }


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    
    # 测试止损计算器
    sl_calc = StopLossCalculator()
    
    print("=== 止损计算测试 ===\n")
    
    # 固定比例止损
    result = sl_calc.calculate_fixed_stop(100.0, 1000, -0.08)
    print(f"固定比例止损:")
    print(f"  止损价：¥{result.stop_price}")
    print(f"  止损幅度：{result.stop_percent}%")
    print(f"  最大亏损：¥{result.loss_amount:,.0f}")
    print(f"  说明：{result.notes}\n")
    
    # 技术位止损
    result = sl_calc.calculate_technical_stop(100.0, 1000, 92.5)
    print(f"技术位止损:")
    print(f"  止损价：¥{result.stop_price}")
    print(f"  止损幅度：{result.stop_percent:.1f}%")
    print(f"  最大亏损：¥{result.loss_amount:,.0f}")
    print(f"  说明：{result.notes}\n")
    
    # 移动止损
    result = sl_calc.calculate_trailing_stop(100.0, 1000, 115.0, 0.05)
    print(f"移动止损:")
    print(f"  止损价：¥{result.stop_price}")
    print(f"  说明：{result.notes}\n")
    
    # 测试止盈计算器
    tp_calc = TakeProfitCalculator()
    
    print("=== 止盈计算测试 ===\n")
    
    # 目标止盈
    result = tp_calc.calculate_target_profit(100.0, 1000, 0.20)
    print(f"目标止盈:")
    print(f"  目标价：¥{result.target_price}")
    print(f"  目标收益：{result.target_percent}%")
    print(f"  预期利润：¥{result.profit_amount:,.0f}")
    print(f"  说明：{result.notes}\n")
    
    # 分批止盈
    results = tp_calc.calculate_batch_exit(100.0, 3000)
    print(f"分批止盈 (3 批):")
    for i, r in enumerate(results, 1):
        print(f"  第{i}批：目标价 ¥{r.target_price} | 利润 ¥{r.profit_amount:,.0f}")
