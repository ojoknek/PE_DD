"""
バリュエーション指標の計算ロジック

README.mdの仕様に基づく、NN_DD評価に必要なバリュエーション計算機能
"""
from typing import Optional


def calculate_net_debt(
    interest_bearing_debt: Optional[float],
    cash_and_equivalents: Optional[float]
) -> Optional[float]:
    """
    Net Debt（純有利子負債）を計算
    
    Args:
        interest_bearing_debt: 有利子負債
        cash_and_equivalents: 現預金
    
    Returns:
        Net Debt（有利子負債−現預金）
    """
    if interest_bearing_debt is None:
        return None
    
    if cash_and_equivalents is None:
        cash_and_equivalents = 0.0
    
    return interest_bearing_debt - cash_and_equivalents


def calculate_enterprise_value_from_ebitda(
    adj_ebitda: Optional[float],
    ebitda_multiple: Optional[float]
) -> Optional[float]:
    """
    EBITDA倍率から企業価値（EV）を計算
    
    Args:
        adj_ebitda: 調整後EBITDA
        ebitda_multiple: EBITDA倍率
    
    Returns:
        企業価値（EV）
    """
    if adj_ebitda is None or ebitda_multiple is None:
        return None
    
    return adj_ebitda * ebitda_multiple


def calculate_equity_value_from_ev(
    enterprise_value: Optional[float],
    net_debt: Optional[float]
) -> Optional[float]:
    """
    企業価値（EV）から株主価値（Equity Value）を計算
    
    Args:
        enterprise_value: 企業価値（EV）
        net_debt: Net Debt
    
    Returns:
        株主価値（Equity Value）
    """
    if enterprise_value is None:
        return None
    
    if net_debt is None:
        net_debt = 0.0
    
    return enterprise_value - net_debt
