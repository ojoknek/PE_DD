#!/usr/bin/env python3
"""
NN DD計算ロジック - 使用例

事業承継ファンドのNN_DD評価における実践的な使用例
"""
import json
from nn_dd_calculator import NNDDCalculator
from financial_metrics import calculate_comprehensive_financial_metrics
from valuation_metrics import (
    calculate_net_debt,
    calculate_enterprise_value_from_ebitda,
    calculate_equity_value_from_ev
)


def example_case_1_pass():
    """例1: 見送りでない案件（合格）"""
    print("\n" + "="*80)
    print("【例1】見送りでない案件（合格）")
    print("="*80)
    
    calc = NNDDCalculator()
    
    # 入力データ
    print("\n■ 入力データ")
    print("  売上高: 600百万円")
    print("  調整後EBITDA: 120百万円")
    print("  Net Debt: 300百万円")
    print("  EBITDA倍率: 4.0倍")
    print("  定性スコア: 適合度4点、ブランド4点、デジタル4点、希少性3点")
    
    # 計算実行
    result = calc.calculate_all(
        sales=600,
        adj_ebitda=120,
        net_debt=300,
        ebitda_multiple=4.0,
        fit_score=4,
        brand_score=4,
        digital_score=4,
        scarcity_score=3
    )
    
    # 結果表示
    print("\n■ 計算結果")
    print(f"  最終判定: {result['final_decision']}")
    print(f"\n  中間計算:")
    print(f"    ND/EBITDA: {result['derived_metrics']['nd_to_ebitda']:.2f}倍")
    print(f"    EV: {result['derived_metrics']['ev']:.0f}百万円")
    print(f"    Equity Value: {result['derived_metrics']['equity_value']:.0f}百万円")
    print(f"    定性合計: {result['derived_metrics']['qualitative_total']}点")
    
    print(f"\n  定量判定:")
    for key, value in result['quantitative_ratings'].items():
        print(f"    {key}: {value}")
    
    print(f"\n  ゲート判定:")
    print(f"    定量: {result['gate_results']['quantitative']}")
    print(f"    定性: {result['gate_results']['qualitative']}")
    
    print("\n✅ この案件はIM取得を推奨します")


def example_case_2_quant_ng():
    """例2: 見送り案件（定量NG）"""
    print("\n" + "="*80)
    print("【例2】見送り案件（定量NG - 売上高不足）")
    print("="*80)
    
    calc = NNDDCalculator()
    
    # 入力データ
    print("\n■ 入力データ")
    print("  売上高: 200百万円 ← 300百万円未満で×判定")
    print("  調整後EBITDA: 80百万円")
    print("  Net Debt: 200百万円")
    print("  EBITDA倍率: 3.5倍")
    print("  定性スコア: 適合度4点、ブランド4点、デジタル4点、希少性3点")
    
    # 計算実行
    result = calc.calculate_all(
        sales=200,  # ×判定
        adj_ebitda=80,
        net_debt=200,
        ebitda_multiple=3.5,
        fit_score=4,
        brand_score=4,
        digital_score=4,
        scarcity_score=3
    )
    
    # 結果表示
    print("\n■ 計算結果")
    print(f"  最終判定: {result['final_decision']}")
    
    if result['reasoning']['quantitative_ng_reasons']:
        print(f"\n  ❌ 定量NG理由:")
        for reason in result['reasoning']['quantitative_ng_reasons']:
            print(f"    - {reason}")
    
    print("\n❌ この案件は見送りです（定量ゲートNG）")


def example_case_3_qual_ng():
    """例3: 見送り案件（定性不合格）"""
    print("\n" + "="*80)
    print("【例3】見送り案件（定性不合格）")
    print("="*80)
    
    calc = NNDDCalculator()
    
    # 入力データ
    print("\n■ 入力データ")
    print("  売上高: 550百万円")
    print("  調整後EBITDA: 110百万円")
    print("  Net Debt: 250百万円")
    print("  EBITDA倍率: 4.0倍")
    print("  定性スコア: 適合度3点、ブランド3点、デジタル2点、希少性2点")
    print("    ← 合計10点（15点未満で不合格）")
    
    # 計算実行
    result = calc.calculate_all(
        sales=550,
        adj_ebitda=110,
        net_debt=250,
        ebitda_multiple=4.0,
        fit_score=3,
        brand_score=3,
        digital_score=2,
        scarcity_score=2
    )
    
    # 結果表示
    print("\n■ 計算結果")
    print(f"  最終判定: {result['final_decision']}")
    print(f"\n  定性評価:")
    print(f"    定性合計: {result['reasoning']['qualitative_score']}点")
    print(f"    合格基準: {result['reasoning']['qualitative_threshold']}点以上")
    print(f"    判定: {result['gate_results']['qualitative']}")
    
    print("\n❌ この案件は見送りです（定性ゲート不合格）")


def example_case_4_comprehensive():
    """例4: 包括的な財務分析との統合"""
    print("\n" + "="*80)
    print("【例4】包括的な財務分析との統合")
    print("="*80)
    
    calc = NNDDCalculator()
    
    # 財務データ
    financial_data = {
        'revenue': 600,
        'revenue_history': [450, 500, 550, 600],  # 過去4年
        'ebitda': 120,
        'operating_income': 100,
        'net_income': 60,
        'equity': 400,
        'total_assets': 800,
        'total_debt': 400,
        'current_assets': 200,
        'current_liabilities': 150,
        'inventory': 50
    }
    
    # 包括的財務指標を計算
    print("\n■ 包括的財務指標")
    financial_metrics = calculate_comprehensive_financial_metrics(financial_data)
    
    print(f"  CAGR: {financial_metrics.get('cagr', 0):.1f}%")
    print(f"  EBITDAマージン: {financial_metrics.get('ebitda_margin', 0):.1f}%")
    print(f"  営業利益率: {financial_metrics.get('operating_margin', 0):.1f}%")
    print(f"  ROE: {financial_metrics.get('roe', 0):.1f}%")
    print(f"  ROA: {financial_metrics.get('roa', 0):.1f}%")
    print(f"  流動比率: {financial_metrics.get('current_ratio', 0):.2f}")
    print(f"  当座比率: {financial_metrics.get('quick_ratio', 0):.2f}")
    print(f"  運転資金: {financial_metrics.get('working_capital', 0):.0f}百万円")
    
    # Net Debt計算
    interest_bearing_debt = 350
    cash = 100
    net_debt = calculate_net_debt(interest_bearing_debt, cash)
    print(f"\n  Net Debt: {net_debt:.0f}百万円")
    
    # NN_DD評価
    print("\n■ NN_DD評価")
    result = calc.calculate_all(
        sales=financial_data['revenue'],
        adj_ebitda=financial_data['ebitda'],
        net_debt=net_debt,
        ebitda_multiple=4.5,
        fit_score=4,
        brand_score=4,
        digital_score=3,
        scarcity_score=4
    )
    
    print(f"  最終判定: {result['final_decision']}")
    print(f"  定量ゲート: {result['gate_results']['quantitative']}")
    print(f"  定性ゲート: {result['gate_results']['qualitative']}")
    
    print("\n✅ 財務分析とNN_DD評価を統合して、包括的な判断が可能です")


def example_case_5_sensitivity():
    """例5: センシティビティ分析"""
    print("\n" + "="*80)
    print("【例5】センシティビティ分析（EBITDA倍率の影響）")
    print("="*80)
    
    calc = NNDDCalculator()
    
    base_sales = 600
    base_ebitda = 120
    base_net_debt = 300
    base_scores = {'fit': 4, 'brand': 4, 'digital': 4, 'scarcity': 3}
    
    print("\n■ EBITDA倍率を変化させた場合の影響")
    print(f"  ベースケース: 売上{base_sales}百万円、EBITDA{base_ebitda}百万円")
    print(f"  定性スコア: {sum(base_scores.values())}点\n")
    
    multiples = [2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5]
    
    print(f"{'倍率':<8} {'EV':<10} {'Equity Value':<15} {'倍率判定':<10} {'最終判定':<12}")
    print("-" * 60)
    
    for multiple in multiples:
        result = calc.calculate_all(
            sales=base_sales,
            adj_ebitda=base_ebitda,
            net_debt=base_net_debt,
            ebitda_multiple=multiple,
            fit_score=base_scores['fit'],
            brand_score=base_scores['brand'],
            digital_score=base_scores['digital'],
            scarcity_score=base_scores['scarcity']
        )
        
        ev = result['derived_metrics']['ev']
        equity = result['derived_metrics']['equity_value']
        multiple_rating = result['quantitative_ratings']['ebitda_multiple']
        decision = result['final_decision']
        
        print(f"{multiple:<8.1f} {ev:<10.0f} {equity:<15.0f} {multiple_rating:<10} {decision:<12}")
    
    print("\n💡 倍率が4.0倍を超えると×判定となり、定量ゲートNGとなります")


def main():
    """メイン処理"""
    print("\n")
    print("="*80)
    print("NN DD計算ロジック - 実践的使用例集")
    print("="*80)
    
    example_case_1_pass()
    example_case_2_quant_ng()
    example_case_3_qual_ng()
    example_case_4_comprehensive()
    example_case_5_sensitivity()
    
    print("\n" + "="*80)
    print("全ての使用例の実行が完了しました")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
