"""
仓位计算器
Position Size Calculator
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class PositionResult:
    """仓位计算结果"""
    recommended_position: float  # 建议仓位比例
    max_position: float  # 最大允许仓位
    actual_position: float  # 实际建议仓位
    shares: int  # 建议股数
    amount: float  # 建议金额
    notes: str

class PositionCalculator:
    """仓位计算器"""
    
    def __init__(self, total_capital: float):
        """
        初始化仓位计算器
        
        Args:
            total_capital: 总资金
        """
        self.total_capital = total_capital
        
        # 仓位限制
        self.limits = {
            "single_stock_max": 0.30,    # 单只股票上限 30%
            "single_industry_max": 0.50, # 单一行业上限 50%
            "max_total_position": 0.80   # 最大总仓位 80%
        }
    
    def calculate_position(self, 
                          risk_level: str,
                          stock_price: float,
                          current_industry_position: float = 0.0,
                          current_total_position: float = 0.0,
                          confidence: float = 0.5) -> PositionResult:
        """
        计算建议仓位
        
        Args:
            risk_level: 风险等级 ("high", "medium_high", "medium", "low", "very_low")
            stock_price: 股票价格
            current_industry_position: 当前该行业已持仓比例
            current_total_position: 当前总仓位比例
            confidence: 信心指数 (0-1)
        
        Returns:
            PositionResult: 仓位计算结果
        """
        # 根据风险等级确定基础仓位
        base_positions = {
            "high": 0.10,
            "medium_high": 0.20,
            "medium": 0.35,
            "low": 0.65,
            "very_low": 0.90
        }
        
        base = base_positions.get(risk_level, 0.35)
        
        # 根据信心指数调整
        adjusted = base * (0.5 + confidence * 0.5)
        
        # 应用单只股票上限
        max_single = self.limits["single_stock_max"]
        capped = min(adjusted, max_single)
        
        # 检查行业集中度
        industry_room = self.limits["single_industry_max"] - current_industry_position
        if industry_room < capped:
            capped = industry_room
        
        # 检查总仓位
        total_room = self.limits["max_total_position"] - current_total_position
        if total_room < capped:
            capped = total_room
        
        # 确保不低于 0
        actual = max(0, capped)
        
        # 计算股数和金额
        if stock_price > 0:
            amount = self.total_capital * actual
            shares = int(amount / stock_price / 100) * 100  # 整百股
        else:
            amount = 0
            shares = 0
        
        # 生成备注
        notes = self._generate_notes(risk_level, actual, max_single, industry_room, total_room)
        
        return PositionResult(
            recommended_position=adjusted,
            max_position=max_single,
            actual_position=actual,
            shares=shares,
            amount=amount,
            notes=notes
        )
    
    def _generate_notes(self, risk_level: str, actual: float, 
                       max_single: float, industry_room: float, 
                       total_room: float) -> str:
        """生成仓位说明"""
        notes = []
        
        if actual < max_single * 0.5:
            notes.append(f"⚠️ 因{risk_level}风险，仓位已下调")
        
        if actual >= industry_room:
            notes.append("⚠️ 已达行业集中度上限")
        
        if actual >= total_room:
            notes.append("⚠️ 已达总仓位上限")
        
        if not notes:
            notes.append("✅ 仓位在安全范围内")
        
        return " | ".join(notes)
    
    def calculate_batch_entry(self,
                             total_position: float,
                             batches: int = 3) -> list:
        """
        计算分批建仓方案
        
        Args:
            total_position: 总仓位比例
            batches: 分批数量
        
        Returns:
            list: 每批仓位比例列表
        """
        if batches <= 0:
            return []
        
        # 等分建仓
        base = total_position / batches
        
        # 金字塔式建仓（第一批最多，后续递减）
        result = []
        remaining = total_position
        
        for i in range(batches):
            if i == batches - 1:
                # 最后一批用剩余全部
                result.append(remaining)
            else:
                # 前几批按比例
                batch = remaining / (batches - i)
                result.append(round(batch, 4))
                remaining -= batch
        
        return result
    
    def set_limits(self, single_stock: float = None, 
                   single_industry: float = None,
                   max_total: float = None):
        """更新仓位限制"""
        if single_stock is not None:
            self.limits["single_stock_max"] = min(1.0, max(0.05, single_stock))
        if single_industry is not None:
            self.limits["single_industry_max"] = min(1.0, max(0.1, single_industry))
        if max_total is not None:
            self.limits["max_total_position"] = min(1.0, max(0.1, max_total))


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    
    # 测试
    calculator = PositionCalculator(total_capital=100000)
    
    # 测试不同风险等级
    for risk in ["high", "medium_high", "medium", "low", "very_low"]:
        result = calculator.calculate_position(
            risk_level=risk,
            stock_price=50.0,
            confidence=0.7
        )
        print(f"\n{risk} 风险:")
        print(f"  建议仓位：{result.actual_position*100:.1f}%")
        print(f"  建议金额：RMB {result.amount:,.0f}")
        print(f"  建议股数：{result.shares} 股")
        print(f"  说明：{result.notes}")
