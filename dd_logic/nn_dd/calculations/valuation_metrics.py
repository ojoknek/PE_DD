"""
バリュエーション指標の計算ロジック
"""
from typing import Dict, Optional


def calculate_ev_sales_multiple(enterprise_value: float, revenue: float) -> float:
    """
    EV/Sales倍率を計算
    
    Args:
        enterprise_value: 企業価値（EV）
        revenue: 売上高
    
    Returns:
        EV/Sales倍率
    """
    if revenue == 0:
        return 0.0
    return enterprise_value / revenue


def calculate_ev_ebitda_multiple(enterprise_value: float, ebitda: float) -> float:
    """
    EV/EBITDA倍率を計算
    
    Args:
        enterprise_value: 企業価値（EV）
        ebitda: EBITDA
    
    Returns:
        EV/EBITDA倍率
    """
    if ebitda == 0:
        return 0.0
    return enterprise_value / ebitda


def calculate_pbr(market_cap: float, book_value: float) -> float:
    """
    PBR（株価純資産倍率）を計算
    
    Args:
        market_cap: 時価総額
        book_value: 純資産
    
    Returns:
        PBR倍率
    """
    if book_value == 0:
        return 0.0
    return market_cap / book_value


def calculate_per(market_cap: float, net_income: float) -> float:
    """
    PER（株価収益率）を計算
    
    Args:
        market_cap: 時価総額
        net_income: 当期純利益
    
    Returns:
        PER倍率
    """
    if net_income == 0:
        return 0.0
    return market_cap / net_income


def calculate_valuation_metrics(valuation_data: Dict) -> Dict:
    """
    バリュエーション指標を一括計算
    
    Args:
        valuation_data: バリュエーションデータ（辞書形式）
    
    Returns:
        計算結果（辞書形式）
    """
    results = {}
    
    # EV/Sales倍率計算
    if 'enterprise_value' in valuation_data and 'revenue' in valuation_data:
        results['ev_sales'] = calculate_ev_sales_multiple(
            valuation_data['enterprise_value'],
            valuation_data['revenue']
        )
    
    # EV/EBITDA倍率計算
    if 'enterprise_value' in valuation_data and 'ebitda' in valuation_data:
        results['ev_ebitda'] = calculate_ev_ebitda_multiple(
            valuation_data['enterprise_value'],
            valuation_data['ebitda']
        )
    
    # PBR計算
    if 'market_cap' in valuation_data and 'book_value' in valuation_data:
        results['pbr'] = calculate_pbr(
            valuation_data['market_cap'],
            valuation_data['book_value']
        )
    
    # PER計算
    if 'market_cap' in valuation_data and 'net_income' in valuation_data:
        results['per'] = calculate_per(
            valuation_data['market_cap'],
            valuation_data['net_income']
        )
    
    return results
