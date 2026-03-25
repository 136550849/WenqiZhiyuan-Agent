"""
风险评分模型
Risk Scoring Model for Investment Analysis
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum

class RiskLevel(Enum):
    """风险等级"""
    HIGH = "🔴 高风险"
    MEDIUM_HIGH = "🟠 中高风险"
    MEDIUM = "🟡 中等风险"
    LOW = "🟢 低风险"
    VERY_LOW = "🔵 极低风险"

@dataclass
class RiskFactor:
    """风险因素"""
    name: str
    score: int  # 0-100
    weight: float  # 权重
    description: str
    level: str  # "high", "medium", "low"

@dataclass
class RiskReport:
    """风险评估报告"""
    stock_name: str
    total_score: float
    risk_level: RiskLevel
    factors: List[RiskFactor]
    recommendations: Dict[str, str]

class RiskScorer:
    """风险评分器"""
    
    def __init__(self):
        # 风险因素权重
        self.weights = {
            "market": 0.25,      # 市场风险权重 25%
            "company": 0.40,     # 公司风险权重 40%
            "financial": 0.25,   # 财务风险权重 25%
            "trading": 0.10      # 交易风险权重 10%
        }
        
        # 风险阈值
        self.thresholds = {
            "high": 70,
            "medium_high": 50,
            "medium": 30,
            "low": 0
        }
    
    def calculate_risk_level(self, score: float) -> RiskLevel:
        """根据评分计算风险等级"""
        if score >= self.thresholds["high"]:
            return RiskLevel.HIGH
        elif score >= self.thresholds["medium_high"]:
            return RiskLevel.MEDIUM_HIGH
        elif score >= self.thresholds["medium"]:
            return RiskLevel.MEDIUM
        elif score >= self.thresholds["low"]:
            return RiskLevel.LOW
        else:
            return RiskLevel.VERY_LOW
    
    def evaluate_market_risk(self, data: Dict) -> List[RiskFactor]:
        """评估市场风险"""
        factors = []
        
        # 大盘走势风险
        market_trend = data.get("market_trend", "neutral")
        trend_scores = {"bull": 20, "neutral": 50, "bear": 80}
        factors.append(RiskFactor(
            name="大盘走势",
            score=trend_scores.get(market_trend, 50),
            weight=0.3,
            description=f"当前市场趋势：{market_trend}",
            level="high" if trend_scores.get(market_trend, 50) > 60 else "low"
        ))
        
        # 行业周期风险
        industry_cycle = data.get("industry_cycle", "mature")
        cycle_scores = {"growth": 30, "mature": 50, "decline": 80}
        factors.append(RiskFactor(
            name="行业周期",
            score=cycle_scores.get(industry_cycle, 50),
            weight=0.3,
            description=f"行业所处周期：{industry_cycle}",
            level="high" if cycle_scores.get(industry_cycle, 50) > 60 else "low"
        ))
        
        # 市场情绪风险
        sentiment = data.get("sentiment", "neutral")
        sentiment_scores = {"optimistic": 40, "neutral": 50, "pessimistic": 70, "panic": 90}
        factors.append(RiskFactor(
            name="市场情绪",
            score=sentiment_scores.get(sentiment, 50),
            weight=0.2,
            description=f"市场情绪：{sentiment}",
            level="high" if sentiment_scores.get(sentiment, 50) > 60 else "low"
        ))
        
        # 流动性风险
        liquidity = data.get("liquidity", "normal")
        liquidity_scores = {"high": 20, "normal": 50, "low": 80}
        factors.append(RiskFactor(
            name="流动性",
            score=liquidity_scores.get(liquidity, 50),
            weight=0.2,
            description=f"流动性状况：{liquidity}",
            level="high" if liquidity_scores.get(liquidity, 50) > 60 else "low"
        ))
        
        return factors
    
    def evaluate_company_risk(self, data: Dict) -> List[RiskFactor]:
        """评估公司风险"""
        factors = []
        
        # 经营风险
        customer_concentration = data.get("customer_concentration", "normal")
        conc_scores = {"low": 30, "normal": 50, "high": 80}
        factors.append(RiskFactor(
            name="客户集中度",
            score=conc_scores.get(customer_concentration, 50),
            weight=0.25,
            description=f"客户集中度：{customer_concentration}",
            level="high" if conc_scores.get(customer_concentration, 50) > 60 else "low"
        ))
        
        # 供应链风险
        supply_chain = data.get("supply_chain", "stable")
        supply_scores = {"stable": 30, "moderate": 50, "risky": 80}
        factors.append(RiskFactor(
            name="供应链稳定性",
            score=supply_scores.get(supply_chain, 50),
            weight=0.25,
            description=f"供应链状况：{supply_chain}",
            level="high" if supply_scores.get(supply_chain, 50) > 60 else "low"
        ))
        
        # 治理风险
        governance = data.get("governance", "good")
        gov_scores = {"good": 30, "average": 50, "poor": 80}
        factors.append(RiskFactor(
            name="公司治理",
            score=gov_scores.get(governance, 50),
            weight=0.25,
            description=f"治理水平：{governance}",
            level="high" if gov_scores.get(governance, 50) > 60 else "low"
        ))
        
        # 法律风险
        legal_risk = data.get("legal_risk", "low")
        legal_scores = {"low": 20, "medium": 50, "high": 90}
        factors.append(RiskFactor(
            name="法律风险",
            score=legal_scores.get(legal_risk, 50),
            weight=0.25,
            description=f"法律风险：{legal_risk}",
            level="high" if legal_scores.get(legal_risk, 50) > 60 else "low"
        ))
        
        return factors
    
    def evaluate_financial_risk(self, data: Dict) -> List[RiskFactor]:
        """评估财务风险"""
        factors = []
        
        # 负债率
        debt_ratio = data.get("debt_ratio", 50)
        debt_score = min(100, max(0, debt_ratio))
        factors.append(RiskFactor(
            name="资产负债率",
            score=debt_score,
            weight=0.3,
            description=f"负债率：{debt_ratio}%",
            level="high" if debt_score > 70 else ("medium" if debt_score > 50 else "low")
        ))
        
        # 现金流
        cash_flow = data.get("cash_flow", "positive")
        cash_scores = {"strong_positive": 20, "positive": 40, "neutral": 50, "negative": 80}
        factors.append(RiskFactor(
            name="现金流状况",
            score=cash_scores.get(cash_flow, 50),
            weight=0.4,
            description=f"现金流：{cash_flow}",
            level="high" if cash_scores.get(cash_flow, 50) > 60 else "low"
        ))
        
        # 盈利能力
        profitability = data.get("profitability", "stable")
        profit_scores = {"strong": 30, "stable": 50, "declining": 70, "loss": 90}
        factors.append(RiskFactor(
            name="盈利能力",
            score=profit_scores.get(profitability, 50),
            weight=0.3,
            description=f"盈利状况：{profitability}",
            level="high" if profit_scores.get(profitability, 50) > 60 else "low"
        ))
        
        return factors
    
    def evaluate_trading_risk(self, data: Dict) -> List[RiskFactor]:
        """评估交易风险"""
        factors = []
        
        # 入场时机
        timing = data.get("entry_timing", "neutral")
        timing_scores = {"excellent": 20, "good": 40, "neutral": 50, "poor": 80}
        factors.append(RiskFactor(
            name="入场时机",
            score=timing_scores.get(timing, 50),
            weight=0.4,
            description=f"入场时机评估：{timing}",
            level="high" if timing_scores.get(timing, 50) > 60 else "low"
        ))
        
        # 仓位风险
        position_size = data.get("position_size", 0.3)
        position_score = min(100, int(position_size * 100 / 0.3 * 50))
        factors.append(RiskFactor(
            name="仓位风险",
            score=position_score,
            weight=0.3,
            description=f"建议仓位：{position_size*100}%",
            level="high" if position_score > 60 else "low"
        ))
        
        # 黑天鹅风险
        black_swan = data.get("black_swan_risk", "low")
        swan_scores = {"low": 30, "medium": 50, "high": 80}
        factors.append(RiskFactor(
            name="黑天鹅风险",
            score=swan_scores.get(black_swan, 50),
            weight=0.3,
            description=f"黑天鹅风险：{black_swan}",
            level="high" if swan_scores.get(black_swan, 50) > 60 else "low"
        ))
        
        return factors
    
    def generate_report(self, stock_name: str, data: Dict) -> RiskReport:
        """生成完整风险评估报告"""
        # 评估各类风险
        market_factors = self.evaluate_market_risk(data)
        company_factors = self.evaluate_company_risk(data)
        financial_factors = self.evaluate_financial_risk(data)
        trading_factors = self.evaluate_trading_risk(data)
        
        # 计算加权分数
        market_score = sum(f.score * f.weight for f in market_factors)
        company_score = sum(f.score * f.weight for f in company_factors)
        financial_score = sum(f.score * f.weight for f in financial_factors)
        trading_score = sum(f.score * f.weight for f in trading_factors)
        
        total_score = (
            market_score * self.weights["market"] +
            company_score * self.weights["company"] +
            financial_score * self.weights["financial"] +
            trading_score * self.weights["trading"]
        )
        
        # 确定风险等级
        risk_level = self.calculate_risk_level(total_score)
        
        # 生成建议
        recommendations = self._generate_recommendations(total_score, risk_level)
        
        # 合并所有因素
        all_factors = market_factors + company_factors + financial_factors + trading_factors
        
        return RiskReport(
            stock_name=stock_name,
            total_score=total_score,
            risk_level=risk_level,
            factors=all_factors,
            recommendations=recommendations
        )
    
    def _generate_recommendations(self, score: float, level: RiskLevel) -> Dict[str, str]:
        """生成风险控制建议"""
        if level == RiskLevel.HIGH:
            return {
                "position": "建议仓位：0-10%，避免参与或极低仓位",
                "stop_loss": "严格止损：-5%",
                "action": "建议：观望或极小仓位试探"
            }
        elif level == RiskLevel.MEDIUM_HIGH:
            return {
                "position": "建议仓位：<20%",
                "stop_loss": "严格止损：-5% 至 -8%",
                "action": "建议：低仓位参与，设置严格止损"
            }
        elif level == RiskLevel.MEDIUM:
            return {
                "position": "建议仓位：20-50%",
                "stop_loss": "标准止损：-8%",
                "action": "建议：中等仓位，分批建仓"
            }
        elif level == RiskLevel.LOW:
            return {
                "position": "建议仓位：50-80%",
                "stop_loss": "宽松止损：-10%",
                "action": "建议：可正常仓位参与"
            }
        else:
            return {
                "position": "建议仓位：80%+",
                "stop_loss": "移动止盈保护",
                "action": "建议：高仓位配置"
            }
    
    def format_report(self, report: RiskReport) -> str:
        """格式化报告输出"""
        lines = []
        lines.append(f"# {report.stock_name} 风险评估报告")
        lines.append("")
        lines.append("## ⚠️ 风险因素识别")
        lines.append("")
        
        # 按风险等级分类因素
        high_risks = [f for f in report.factors if f.level == "high"]
        medium_risks = [f for f in report.factors if f.level == "medium"]
        low_risks = [f for f in report.factors if f.level == "low"]
        
        if high_risks:
            lines.append("### 高风险因素")
            for f in high_risks:
                lines.append(f"1. {f.name}: {f.description} (评分：{f.score})")
            lines.append("")
        
        if medium_risks:
            lines.append("### 中风险因素")
            for f in medium_risks:
                lines.append(f"1. {f.name}: {f.description} (评分：{f.score})")
            lines.append("")
        
        if low_risks:
            lines.append("### 低风险因素")
            for f in low_risks:
                lines.append(f"1. {f.name}: {f.description} (评分：{f.score})")
            lines.append("")
        
        lines.append("## 📊 风险等级")
        lines.append(f"**综合风险等级**：{report.risk_level.value}")
        lines.append(f"**风险评分**：{report.total_score:.1f} / 100")
        lines.append("")
        
        lines.append("## 🛡️ 风险控制建议")
        lines.append("")
        lines.append("### 仓位建议")
        lines.append(f"- {report.recommendations['position']}")
        lines.append(f"- 建仓方式：分批建仓")
        lines.append("")
        lines.append("### 止损建议")
        lines.append(f"- {report.recommendations['stop_loss']}")
        lines.append("")
        lines.append("### 监控要点")
        lines.append("- 需要重点关注的风险指标：")
        for f in report.factors[:3]:
            lines.append(f"  - {f.name}")
        lines.append("")
        
        lines.append("## 📝 风险总结")
        lines.append(f"综合评分 {report.total_score:.1f} 分，属于{report.risk_level.value}。")
        lines.append(f"{report.recommendations['action']}")
        
        return "\n".join(lines)


# 快捷使用
if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    
    scorer = RiskScorer()
    
    # 测试数据
    test_data = {
        "market_trend": "neutral",
        "industry_cycle": "mature",
        "sentiment": "neutral",
        "liquidity": "normal",
        "customer_concentration": "normal",
        "supply_chain": "stable",
        "governance": "good",
        "legal_risk": "low",
        "debt_ratio": 45,
        "cash_flow": "positive",
        "profitability": "stable",
        "entry_timing": "good",
        "position_size": 0.25,
        "black_swan_risk": "low"
    }
    
    report = scorer.generate_report("测试股票", test_data)
    print(scorer.format_report(report))
