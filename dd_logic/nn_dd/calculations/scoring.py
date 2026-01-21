"""
スコアリングロジック
"""
from typing import Dict, List, Optional


def score_business_overview(data: Dict) -> float:
    """
    事業概要のスコアリング
    
    Args:
        data: 事業概要データ
    
    Returns:
        スコア（0-100）
    """
    score = 0.0
    
    # 事業内容の明確性（0-30点）
    if 'business_description' in data and data['business_description']:
        score += 15
    if 'business_model' in data and data['business_model']:
        score += 15
    
    # 市場規模・成長性（0-40点）
    if 'market_size' in data and data['market_size']:
        score += 20
    if 'market_growth' in data and data['market_growth']:
        score += 20
    
    # ビジネスモデル（0-30点）
    if 'revenue_model' in data and data['revenue_model']:
        score += 30
    
    return min(score, 100.0)


def score_financial_info(data: Dict) -> float:
    """
    財務情報のスコアリング
    
    Args:
        data: 財務情報データ
    
    Returns:
        スコア（0-100）
    """
    score = 0.0
    
    # 売上規模（0-25点）
    if 'revenue' in data:
        revenue = data['revenue']
        if revenue >= 10000000000:  # 100億円以上
            score += 25
        elif revenue >= 1000000000:  # 10億円以上
            score += 20
        elif revenue >= 100000000:  # 1億円以上
            score += 15
        else:
            score += 10
    
    # 成長率（0-25点）
    if 'growth_rate' in data:
        growth_rate = data['growth_rate']
        if growth_rate >= 50:
            score += 25
        elif growth_rate >= 30:
            score += 20
        elif growth_rate >= 20:
            score += 15
        else:
            score += 10
    
    # 収益性（0-25点）
    if 'ebitda_margin' in data:
        margin = data['ebitda_margin']
        if margin >= 20:
            score += 25
        elif margin >= 15:
            score += 20
        elif margin >= 10:
            score += 15
        else:
            score += 10
    
    # 財務健全性（0-25点）
    if 'debt_ratio' in data:
        debt_ratio = data['debt_ratio']
        if debt_ratio <= 30:
            score += 25
        elif debt_ratio <= 50:
            score += 20
        elif debt_ratio <= 70:
            score += 15
        else:
            score += 10
    
    return min(score, 100.0)


def score_management_team(data: Dict) -> float:
    """
    経営陣・組織のスコアリング
    
    Args:
        data: 経営陣・組織データ
    
    Returns:
        スコア（0-100）
    """
    score = 0.0
    
    # 経営陣の経験・実績（0-50点）
    if 'management_experience' in data:
        experience = data['management_experience']
        if experience >= 10:
            score += 50
        elif experience >= 5:
            score += 40
        elif experience >= 3:
            score += 30
        else:
            score += 20
    
    # 組織体制（0-30点）
    if 'organization_structure' in data and data['organization_structure']:
        score += 30
    
    # 人材構成（0-20点）
    if 'team_size' in data:
        team_size = data['team_size']
        if team_size >= 50:
            score += 20
        elif team_size >= 20:
            score += 15
        else:
            score += 10
    
    return min(score, 100.0)


def score_market_competition(data: Dict) -> float:
    """
    市場・競合のスコアリング
    
    Args:
        data: 市場・競合データ
    
    Returns:
        スコア（0-100）
    """
    score = 0.0
    
    # 市場ポジション（0-40点）
    if 'market_position' in data:
        position = data['market_position']
        if position == 'leader':
            score += 40
        elif position == 'top3':
            score += 30
        elif position == 'top10':
            score += 20
        else:
            score += 10
    
    # 競合優位性（0-30点）
    if 'competitive_advantage' in data and data['competitive_advantage']:
        score += 30
    
    # 市場成長性（0-30点）
    if 'market_growth' in data:
        growth = data['market_growth']
        if growth >= 20:
            score += 30
        elif growth >= 10:
            score += 20
        else:
            score += 10
    
    return min(score, 100.0)


def score_investment_terms(data: Dict) -> float:
    """
    投資条件のスコアリング
    
    Args:
        data: 投資条件データ
    
    Returns:
        スコア（0-100）
    """
    score = 0.0
    
    # 投資規模（0-25点）
    if 'investment_amount' in data:
        amount = data['investment_amount']
        if amount >= 1000000000:  # 10億円以上
            score += 25
        elif amount >= 100000000:  # 1億円以上
            score += 20
        else:
            score += 15
    
    # バリュエーション（0-25点）
    if 'valuation' in data:
        # バリュエーションの妥当性を評価
        score += 25
    
    # 投資期間（0-25点）
    if 'investment_period' in data:
        period = data['investment_period']
        if 3 <= period <= 7:
            score += 25
        else:
            score += 15
    
    # 出口戦略（0-25点）
    if 'exit_strategy' in data and data['exit_strategy']:
        score += 25
    
    return min(score, 100.0)


def calculate_total_score(scores: Dict[str, float], weights: Optional[Dict[str, float]] = None) -> float:
    """
    総合スコアを計算
    
    Args:
        scores: 各論点のスコア
        weights: 各論点の重み（デフォルトは均等）
    
    Returns:
        総合スコア（0-100）
    """
    if weights is None:
        weights = {
            'business_overview': 0.2,
            'financial_info': 0.25,
            'management_team': 0.2,
            'market_competition': 0.15,
            'investment_terms': 0.2
        }
    
    total_score = 0.0
    total_weight = 0.0
    
    for key, score in scores.items():
        if key in weights:
            total_score += score * weights[key]
            total_weight += weights[key]
    
    if total_weight > 0:
        return total_score / total_weight
    return 0.0


def calculate_risk_score(data: Dict) -> float:
    """
    リスクスコアを計算
    
    Args:
        data: リスクデータ
    
    Returns:
        リスクスコア（0-100、高いほどリスクが高い）
    """
    risk_score = 0.0
    
    # 事業リスク（0-30点）
    if 'business_risk' in data:
        risk_score += data['business_risk'] * 0.3
    
    # 財務リスク（0-30点）
    if 'financial_risk' in data:
        risk_score += data['financial_risk'] * 0.3
    
    # 市場リスク（0-20点）
    if 'market_risk' in data:
        risk_score += data['market_risk'] * 0.2
    
    # その他リスク（0-20点）
    if 'other_risk' in data:
        risk_score += data['other_risk'] * 0.2
    
    return min(risk_score, 100.0)
