"""
財務指標の計算ロジック

事業承継ファンド向けに拡張された財務指標計算機能
"""
from typing import Dict, Optional, List


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


def calculate_debt_to_equity_ratio(
    total_debt: Optional[float],
    equity: Optional[float]
) -> Optional[float]:
    """
    負債資本比率（Debt-to-Equity Ratio）を計算
    
    Args:
        total_debt: 総負債
        equity: 自己資本
    
    Returns:
        負債資本比率（%）
    """
    if equity is None or equity == 0:
        return None
    
    if total_debt is None:
        return 0.0
    
    return (total_debt / equity) * 100


def calculate_current_ratio(
    current_assets: Optional[float],
    current_liabilities: Optional[float]
) -> Optional[float]:
    """
    流動比率を計算
    
    Args:
        current_assets: 流動資産
        current_liabilities: 流動負債
    
    Returns:
        流動比率
    """
    if current_liabilities is None or current_liabilities == 0:
        return None
    
    if current_assets is None:
        return 0.0
    
    return current_assets / current_liabilities


def calculate_quick_ratio(
    current_assets: Optional[float],
    inventory: Optional[float],
    current_liabilities: Optional[float]
) -> Optional[float]:
    """
    当座比率を計算
    
    Args:
        current_assets: 流動資産
        inventory: 在庫
        current_liabilities: 流動負債
    
    Returns:
        当座比率
    """
    if current_liabilities is None or current_liabilities == 0:
        return None
    
    if current_assets is None:
        current_assets = 0.0
    
    if inventory is None:
        inventory = 0.0
    
    quick_assets = current_assets - inventory
    return quick_assets / current_liabilities


def calculate_working_capital(
    current_assets: Optional[float],
    current_liabilities: Optional[float]
) -> Optional[float]:
    """
    運転資金を計算
    
    Args:
        current_assets: 流動資産
        current_liabilities: 流動負債
    
    Returns:
        運転資金
    """
    if current_assets is None or current_liabilities is None:
        return None
    
    return current_assets - current_liabilities


def calculate_working_capital_turnover(
    revenue: Optional[float],
    working_capital: Optional[float]
) -> Optional[float]:
    """
    運転資金回転率を計算
    
    Args:
        revenue: 売上高
        working_capital: 運転資金
    
    Returns:
        運転資金回転率
    """
    if working_capital is None or working_capital == 0:
        return None
    
    if revenue is None:
        return None
    
    return revenue / working_capital


def calculate_comprehensive_financial_metrics(financial_data: Dict) -> Dict:
    """
    包括的な財務指標を一括計算
    
    Args:
        financial_data: 財務データ（辞書形式）
            - revenue: 売上高
            - revenue_history: 売上高の履歴（リスト）
            - ebitda: EBITDA
            - operating_income: 営業利益
            - net_income: 当期純利益
            - equity: 自己資本
            - total_assets: 総資産
            - total_debt: 総負債
            - current_assets: 流動資産
            - current_liabilities: 流動負債
            - inventory: 在庫
    
    Returns:
        計算結果（辞書形式）
    """
    results = {}
    
    # 基本指標
    basic_metrics = calculate_financial_metrics(financial_data)
    results.update(basic_metrics)
    
    # 負債資本比率
    if 'total_debt' in financial_data and 'equity' in financial_data:
        results['debt_to_equity_ratio'] = calculate_debt_to_equity_ratio(
            financial_data['total_debt'],
            financial_data['equity']
        )
    
    # 流動比率
    if 'current_assets' in financial_data and 'current_liabilities' in financial_data:
        results['current_ratio'] = calculate_current_ratio(
            financial_data['current_assets'],
            financial_data['current_liabilities']
        )
    
    # 当座比率
    if 'current_assets' in financial_data and 'current_liabilities' in financial_data:
        inventory = financial_data.get('inventory', 0)
        results['quick_ratio'] = calculate_quick_ratio(
            financial_data['current_assets'],
            inventory,
            financial_data['current_liabilities']
        )
    
    # 運転資金
    if 'current_assets' in financial_data and 'current_liabilities' in financial_data:
        results['working_capital'] = calculate_working_capital(
            financial_data['current_assets'],
            financial_data['current_liabilities']
        )
        
        # 運転資金回転率
        if 'revenue' in financial_data:
            results['working_capital_turnover'] = calculate_working_capital_turnover(
                financial_data['revenue'],
                results['working_capital']
            )
    
    return results
