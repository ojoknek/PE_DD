"""
DCF（Discounted Cash Flow）分析の計算ロジック
"""
from typing import Dict, List, Optional


def calculate_dcf(
    free_cash_flows: List[float],
    terminal_value: float,
    discount_rate: float,
    terminal_growth_rate: float = 0.03
) -> Dict:
    """
    DCF分析を実行
    
    Args:
        free_cash_flows: フリーキャッシュフローのリスト
        terminal_value: ターミナルバリュー
        discount_rate: 割引率（WACC等）
        terminal_growth_rate: ターミナル成長率（デフォルト3%）
    
    Returns:
        DCF分析結果（辞書形式）
    """
    # 予測期間のDCF計算
    pv_fcf = []
    for i, fcf in enumerate(free_cash_flows):
        pv = fcf / ((1 + discount_rate) ** (i + 1))
        pv_fcf.append(pv)
    
    # ターミナルバリューの現在価値
    terminal_period = len(free_cash_flows)
    pv_terminal = terminal_value / ((1 + discount_rate) ** terminal_period)
    
    # 企業価値（EV）
    enterprise_value = sum(pv_fcf) + pv_terminal
    
    return {
        'enterprise_value': enterprise_value,
        'pv_fcf': sum(pv_fcf),
        'pv_terminal': pv_terminal,
        'discount_rate': discount_rate,
        'terminal_growth_rate': terminal_growth_rate
    }


def calculate_terminal_value(
    final_fcf: float,
    terminal_growth_rate: float,
    discount_rate: float
) -> float:
    """
    ターミナルバリューを計算（Gordon Growth Model）
    
    Args:
        final_fcf: 最終年度のフリーキャッシュフロー
        terminal_growth_rate: ターミナル成長率
        discount_rate: 割引率
    
    Returns:
        ターミナルバリュー
    """
    if discount_rate <= terminal_growth_rate:
        return 0.0
    return final_fcf * (1 + terminal_growth_rate) / (discount_rate - terminal_growth_rate)


def calculate_wacc(
    equity_value: float,
    debt_value: float,
    cost_of_equity: float,
    cost_of_debt: float,
    tax_rate: float
) -> float:
    """
    WACC（加重平均資本コスト）を計算
    
    Args:
        equity_value: 株式価値
        debt_value: 負債価値
        cost_of_equity: 資本コスト
        cost_of_debt: 負債コスト
        tax_rate: 税率
    
    Returns:
        WACC
    """
    total_value = equity_value + debt_value
    if total_value == 0:
        return 0.0
    
    equity_weight = equity_value / total_value
    debt_weight = debt_value / total_value
    
    wacc = (equity_weight * cost_of_equity) + (debt_weight * cost_of_debt * (1 - tax_rate))
    return wacc


def sensitivity_analysis(
    base_fcf: List[float],
    base_terminal_value: float,
    base_discount_rate: float,
    discount_rate_range: List[float],
    growth_rate_range: List[float]
) -> Dict:
    """
    感度分析を実行
    
    Args:
        base_fcf: ベースケースのフリーキャッシュフロー
        base_terminal_value: ベースケースのターミナルバリュー
        base_discount_rate: ベースケースの割引率
        discount_rate_range: 割引率の範囲
        growth_rate_range: 成長率の範囲
    
    Returns:
        感度分析結果（辞書形式）
    """
    results = {}
    
    for dr in discount_rate_range:
        for gr in growth_rate_range:
            key = f"dr_{dr}_gr_{gr}"
            dcf_result = calculate_dcf(
                base_fcf,
                base_terminal_value,
                dr,
                gr
            )
            results[key] = dcf_result['enterprise_value']
    
    return results
