#!/usr/bin/env python3
"""
事業承継ファンド評価論点管理システム - 実践例

実際のDD業務でどのように使用するかの具体例を示します。
"""

from evaluation_points_manager import EvaluationPointsManager
from pathlib import Path


def example_nn_dd_screening():
    """
    例1: NN_DD段階でのスクリーニング評価
    
    ティーザーやノンネーム資料から得られた情報を基に、
    IM取得判断を行う際の使用例
    """
    print("\n" + "="*80)
    print("【例1】NN_DD段階でのスクリーニング評価")
    print("="*80 + "\n")
    
    manager = EvaluationPointsManager()
    
    # 案件概要（架空の事例）
    print("■ 案件概要")
    print("  業種: 製造業（金属加工）")
    print("  売上: 15億円、EBITDA: 2.5億円")
    print("  創業: 1985年、創業者70歳")
    print("  従業員: 80名\n")
    
    # クリティカル論点をチェック
    print("■ クリティカル論点の確認")
    critical = manager.get_critical_points('nn_dd')
    
    print("\n【定量クリティカル論点】")
    for point_name in critical['quantitative'].keys():
        print(f"  ✓ {point_name}")
    
    print("\n【定性クリティカル論点】")
    for point_name in critical['qualitative'].keys():
        print(f"  ✓ {point_name}")
    
    # 各論点のスコア付け（仮想データ）
    print("\n■ 評価スコア（0-100点）")
    
    # 定量論点の評価
    quant_scores = {
        'financial_performance': 82,  # 安定した収益実績
        'financial_health': 68,       # 負債がやや多いが許容範囲
        'market_size': 75,            # ニッチ市場で安定需要
        'preliminary_valuation': 72   # EV/EBITDA 6倍で妥当
    }
    
    quant_score, quant_details = manager.calculate_category_score(
        'nn_dd', 'quantitative', quant_scores
    )
    
    print(f"\n【定量論点】 総合スコア: {quant_score:.1f}点")
    for point, detail in quant_details.items():
        critical_mark = "★" if detail['critical'] else " "
        print(f"  {critical_mark} {point}: {detail['score']:.0f}点 (ウェイト {detail['weight']:.0%})")
    
    # 定性論点の評価
    qual_scores = {
        'succession_background': 88,  # 明確な後継者不在、承継ニーズ高
        'business_model': 78,         # 技術力があり参入障壁あり
        'management_organization': 62, # 創業者依存度が高い
        'business_relationships': 70,  # 取引先は分散、長期関係
        'investment_fit': 80          # ファンド戦略と合致
    }
    
    qual_score, qual_details = manager.calculate_category_score(
        'nn_dd', 'qualitative', qual_scores
    )
    
    print(f"\n【定性論点】 総合スコア: {qual_score:.1f}点")
    for point, detail in qual_details.items():
        critical_mark = "★" if detail['critical'] else " "
        print(f"  {critical_mark} {point}: {detail['score']:.0f}点 (ウェイト {detail['weight']:.0%})")
    
    # 総合判断
    print("\n■ 総合判断")
    overall = quant_score * 0.55 + qual_score * 0.45  # 定量55%, 定性45%
    print(f"  NN_DD総合スコア: {overall:.1f}点")
    
    if overall >= 75 and quant_score >= 70 and qual_score >= 70:
        decision = "【判定】 IM取得を強く推奨 ✓"
    elif overall >= 65:
        decision = "【判定】 IM取得を検討（条件付き）"
    else:
        decision = "【判定】 見送り推奨"
    
    print(f"\n  {decision}")
    
    # 次のアクションアイテム
    print("\n■ 次のアクションアイテム")
    print("  1. IM取得の申し込み")
    print("  2. 経営陣との初回面談設定")
    print("  3. 財務DD・法務DD業者の選定")
    print("  4. 投資委員会への案件説明準備")


def example_im_dd_checklist():
    """
    例2: IM_DD段階でのチェックリスト作成
    
    IMを取得した後、詳細DDを実施する際のチェックリスト生成例
    """
    print("\n" + "="*80)
    print("【例2】IM_DD段階でのチェックリスト作成")
    print("="*80 + "\n")
    
    manager = EvaluationPointsManager()
    
    # 事業承継特有論点を確認
    print("■ 事業承継特有論点の重点確認項目")
    succession = manager.get_succession_specific_points('im_dd')
    
    for point_name, point_data in succession.items():
        print(f"\n【{point_name}】")
        for i, sub in enumerate(point_data['sub_points'], 1):
            print(f"  {i}. □ {sub}")
        
        sources = point_data.get('data_sources', [])
        print(f"  📊 必要資料: {', '.join(sources)}")
    
    # クリティカル論点のチェックリスト
    print("\n\n■ クリティカル論点チェックリスト（定量）")
    critical_quant = manager.get_critical_points('im_dd', 'quantitative')
    
    item_count = 0
    for point_name, point_data in critical_quant.items():
        print(f"\n【{point_name}】")
        for sub in point_data['sub_points']:
            item_count += 1
            print(f"  {item_count}. □ {sub}")
    
    print("\n\n■ クリティカル論点チェックリスト（定性）")
    critical_qual = manager.get_critical_points('im_dd', 'qualitative')
    
    for point_name, point_data in critical_qual.items():
        print(f"\n【{point_name}】")
        for sub in point_data['sub_points']:
            item_count += 1
            print(f"  {item_count}. □ {sub}")
    
    print(f"\n\n📋 総チェック項目数: {item_count}項目")


def example_comparison_analysis():
    """
    例3: 複数案件の比較分析
    
    同時に検討している複数案件を比較する際の使用例
    """
    print("\n" + "="*80)
    print("【例3】複数案件の比較分析")
    print("="*80 + "\n")
    
    manager = EvaluationPointsManager()
    
    # 案件A（製造業）
    deal_a_quant = {
        'financial_performance': 85,
        'financial_health': 90,
        'market_size': 70,
        'preliminary_valuation': 75
    }
    deal_a_qual = {
        'succession_background': 90,
        'business_model': 80,
        'management_organization': 65,
        'business_relationships': 75,
        'investment_fit': 85
    }
    
    # 案件B（サービス業）
    deal_b_quant = {
        'financial_performance': 78,
        'financial_health': 85,
        'market_size': 85,
        'preliminary_valuation': 70
    }
    deal_b_qual = {
        'succession_background': 85,
        'business_model': 75,
        'management_organization': 70,
        'business_relationships': 80,
        'investment_fit': 75
    }
    
    # スコア計算
    a_quant, _ = manager.calculate_category_score('nn_dd', 'quantitative', deal_a_quant)
    a_qual, _ = manager.calculate_category_score('nn_dd', 'qualitative', deal_a_qual)
    a_overall = a_quant * 0.55 + a_qual * 0.45
    
    b_quant, _ = manager.calculate_category_score('nn_dd', 'quantitative', deal_b_quant)
    b_qual, _ = manager.calculate_category_score('nn_dd', 'qualitative', deal_b_qual)
    b_overall = b_quant * 0.55 + b_qual * 0.45
    
    # 比較表を作成
    print("■ 案件比較サマリー\n")
    print(f"{'項目':<20} {'案件A（製造業）':>15} {'案件B（サービス業）':>20}")
    print("-" * 60)
    print(f"{'定量論点':20} {a_quant:>15.1f}点 {b_quant:>20.1f}点")
    print(f"{'定性論点':20} {a_qual:>15.1f}点 {b_qual:>20.1f}点")
    print("-" * 60)
    print(f"{'総合スコア':20} {a_overall:>15.1f}点 {b_qual:>20.1f}点")
    print()
    
    # 推奨順位
    if a_overall > b_overall:
        print("【推奨】 案件A を優先的に検討")
        print(f"  理由: 総合スコアが {a_overall - b_overall:.1f}点高い")
        if a_quant > b_quant:
            print(f"  特に定量面で優位（+{a_quant - b_quant:.1f}点）")
    else:
        print("【推奨】 案件B を優先的に検討")
        print(f"  理由: 総合スコアが {b_overall - a_overall:.1f}点高い")
        if b_quant > a_quant:
            print(f"  特に定量面で優位（+{b_quant - a_quant:.1f}点）")


def example_export_framework():
    """
    例4: 評価フレームワークのエクスポート
    
    評価フレームワークをMarkdown形式でエクスポートし、
    チーム内で共有する際の使用例
    """
    print("\n" + "="*80)
    print("【例4】評価フレームワークのエクスポート")
    print("="*80 + "\n")
    
    manager = EvaluationPointsManager()
    
    # 出力ディレクトリの確認
    output_dir = Path(__file__).parent / 'outputs'
    output_dir.mkdir(exist_ok=True)
    
    # NN_DDフレームワークをエクスポート
    nn_dd_path = output_dir / 'nn_dd_evaluation_framework.md'
    manager.export_to_markdown('nn_dd', nn_dd_path)
    
    # IM_DDフレームワークをエクスポート
    im_dd_path = output_dir / 'im_dd_evaluation_framework.md'
    manager.export_to_markdown('im_dd', im_dd_path)
    
    print(f"\n✅ 出力完了")
    print(f"  - {nn_dd_path}")
    print(f"  - {im_dd_path}")
    print("\nこれらのファイルをチーム内で共有して、評価基準の統一を図ることができます。")


def main():
    """メイン処理"""
    print("\n")
    print("="*80)
    print("事業承継ファンド評価論点管理システム - 実践例集")
    print("="*80)
    
    # 各例を実行
    example_nn_dd_screening()
    example_im_dd_checklist()
    example_comparison_analysis()
    example_export_framework()
    
    print("\n\n" + "="*80)
    print("全ての実践例の実行が完了しました")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
