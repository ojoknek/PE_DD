"""
財務指標の計算ロジック
"""
from typing import Dict, Optional


def calculate_cagr(start_value: float, end_value: float, periods: int) -> float:
    """
    売上成長率（CAGR）を計算
    
    Args:
        start_value: 開始値
        end_value: 終了値
        periods: 期間数（年）
    
    Returns:
        CAGR（%）
    """
    if start_value <= 0 or periods <= 0:
        return 0.0
    return ((end_value / start_value) ** (1 / periods) - 1) * 100


def calculate_ebitda_margin(ebitda: float, revenue: float) -> float:
    """
    EBITDAマージンを計算
    
    Args:
        ebitda: EBITDA
        revenue: 売上高
    
    Returns:
        EBITDAマージン（%）
    """
    if revenue == 0:
        return 0.0
    return (ebitda / revenue) * 100


def calculate_operating_margin(operating_income: float, revenue: float) -> float:
    """
    営業利益率を計算
    
    Args:
        operating_income: 営業利益
        revenue: 売上高
    
    Returns:
        営業利益率（%）
    """
    if revenue == 0:
        return 0.0
    return (operating_income / revenue) * 100


def calculate_roe(net_income: float, equity: float) -> float:
    """
    ROE（自己資本利益率）を計算
    
    Args:
        net_income: 当期純利益
        equity: 自己資本
    
    Returns:
        ROE（%）
    """
    if equity == 0:
        return 0.0
    return (net_income / equity) * 100


def calculate_roa(net_income: float, total_assets: float) -> float:
    """
    ROA（総資産利益率）を計算
    
    Args:
        net_income: 当期純利益
        total_assets: 総資産
    
    Returns:
        ROA（%）
    """
    if total_assets == 0:
        return 0.0
    return (net_income / total_assets) * 100


def calculate_financial_metrics(financial_data: Dict) -> Dict:
    """
    財務指標を一括計算
    
    Args:
        financial_data: 財務データ（辞書形式）
    
    Returns:
        計算結果（辞書形式）
    """
    results = {}
    
    # CAGR計算
    if 'revenue_history' in financial_data:
        revenue_history = financial_data['revenue_history']
        if len(revenue_history) >= 2:
            start_revenue = revenue_history[0]
            end_revenue = revenue_history[-1]
            periods = len(revenue_history) - 1
            results['cagr'] = calculate_cagr(start_revenue, end_revenue, periods)
    
    # EBITDAマージン計算
    if 'ebitda' in financial_data and 'revenue' in financial_data:
        results['ebitda_margin'] = calculate_ebitda_margin(
            financial_data['ebitda'],
            financial_data['revenue']
        )
    
    # 営業利益率計算
    if 'operating_income' in financial_data and 'revenue' in financial_data:
        results['operating_margin'] = calculate_operating_margin(
            financial_data['operating_income'],
            financial_data['revenue']
        )
    
    # ROE計算
    if 'net_income' in financial_data and 'equity' in financial_data:
        results['roe'] = calculate_roe(
            financial_data['net_income'],
            financial_data['equity']
        )
    
    # ROA計算
    if 'net_income' in financial_data and 'total_assets' in financial_data:
        results['roa'] = calculate_roa(
            financial_data['net_income'],
            financial_data['total_assets']
        )
    
    return results
