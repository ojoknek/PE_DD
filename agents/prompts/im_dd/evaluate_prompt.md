# IM DD評価プロンプト

## 目的
構造化されたIMデータを基に、IM DD評価を実行します。定量情報と定性情報を統合し、一定の結論を導出します。

## 入力
- 構造化されたIMデータ（JSON形式）
- 評価論点（`dd_logic/im_dd/evaluation_points/evaluation_points.md`を参照）

## 処理手順
1. 各評価論点について評価を実行（定量・定性情報の統合）：
   - 事業性評価（定量・定性情報の統合）
   - 財務評価（定量情報の分析）
   - 経営陣評価（定性情報の評価）
   - リスク評価（定量・定性情報の統合）
   - 投資条件評価（定量情報の分析）
2. 計算ロジックを適用：
   - DCF分析（定量情報）
   - バリュエーション分析（定量情報）
   - リスク分析（定量・定性情報の統合）
   - スコアリング（定量・定性情報の統合）
3. 定量・定性情報を統合した結論の導出
4. 各論点の評価結果を出力

## 出力形式
JSON形式で以下の構造で出力：
```json
{
  "evaluation_results": {
    "business_evaluation": {
      "score": 0,
      "evaluation": "...",
      "details": "...",
      "comments": "..."
    },
    "financial_evaluation": {
      "score": 0,
      "evaluation": "...",
      "details": "...",
      "comments": "...",
      "dcf_analysis": {...},
      "valuation_analysis": {...}
    },
    "management_evaluation": {
      "score": 0,
      "evaluation": "...",
      "details": "...",
      "comments": "..."
    },
    "risk_evaluation": {
      "score": 0,
      "evaluation": "...",
      "details": "...",
      "comments": "...",
      "risk_factors": [...]
    },
    "investment_terms_evaluation": {
      "score": 0,
      "evaluation": "...",
      "details": "...",
      "comments": "..."
    }
  },
  "total_score": 0,
  "investment_recommendation": "...",
  "key_risks": [...]
}
```

## 注意事項
- 各論点のスコアは0-100の範囲で算出
- 総合スコアは重み付け平均で算出
- 定量情報と定性情報を統合した結論を明確に示す
- 投資推奨度は総合スコアとリスク評価に基づいて決定
- 参考文献（`dd_logic/references/`）を参照して評価ロジックを適用