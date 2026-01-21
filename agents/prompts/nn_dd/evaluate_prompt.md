# NN DD評価プロンプト

## 目的
構造化されたデータを基に、NN DD評価を実行します。定量情報と定性情報を統合し、一定の結論を導出します。

## 入力
- 構造化されたデータ（JSON形式）
- 評価基準（`dd_logic/nn_dd/criteria/evaluation_criteria.md`を参照）

## 処理手順
1. 各評価論点について評価を実行：
   - 事業概要（定量・定性情報の統合）
   - 財務情報（定量情報の分析）
   - 経営陣・組織（定性情報の評価）
   - 市場・競合（定量・定性情報の統合）
   - 投資条件（定量情報の分析）
2. 計算ロジックを適用：
   - 財務指標の計算（定量情報）
   - バリュエーション指標の計算（定量情報）
   - スコアリング（定量・定性情報の統合）
3. 定量・定性情報を統合した結論の導出
4. 各論点の評価結果を出力

## 出力形式
JSON形式で以下の構造で出力：
```json
{
  "evaluation_results": {
    "business_overview": {
      "score": 0,
      "evaluation": "...",
      "comments": "..."
    },
    "financial_info": {
      "score": 0,
      "evaluation": "...",
      "comments": "...",
      "metrics": {
        "cagr": 0,
        "ebitda_margin": 0,
        "operating_margin": 0,
        "roe": 0,
        "roa": 0
      }
    },
    "management_team": {
      "score": 0,
      "evaluation": "...",
      "comments": "..."
    },
    "market_competition": {
      "score": 0,
      "evaluation": "...",
      "comments": "..."
    },
    "investment_terms": {
      "score": 0,
      "evaluation": "...",
      "comments": "...",
      "valuation_metrics": {
        "ev_sales": 0,
        "ev_ebitda": 0,
        "pbr": 0,
        "per": 0
      }
    }
  },
  "total_score": 0,
  "risk_score": 0,
  "recommendation": "..."
}
```

## 注意事項
- 各論点のスコアは0-100の範囲で算出
- 総合スコアは重み付け平均で算出
- 定量情報と定性情報を統合した結論を明確に示す
- 推奨アクションは総合スコアとリスクスコアに基づいて決定
- 参考文献（`dd_logic/references/`）を参照して評価ロジックを適用