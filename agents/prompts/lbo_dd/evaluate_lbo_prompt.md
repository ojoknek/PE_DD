# LBO DD評価プロンプト

## 目的
構築されたLBOモデルを基に、LBO DD評価を実行します。定量情報と定性情報を統合し、実行判断（実行推奨/条件付き実行/実行見送り）を導出します。

## 入力
- 構築されたLBOモデル（JSON形式、`build_lbo_model_prompt.md`の出力）
- 構造化されたVDRデータ（JSON形式、`load_vdr_prompt.md`の出力）
- 評価論点（`dd_logic/lbo_dd/evaluation_points/evaluation_points.md`を参照）

## 処理手順

### 1. 各評価論点について評価を実行

#### 1.1 定量論点（ウェイト合計: 60%）

##### LBOモデル構築（25%）★クリティカル
- レバレッジ比率の設定の妥当性
- 負債スケジュールの構築の適切性
- 財務3表の構築の正確性
- スコア: 0-100点

##### リターン分析（20%）★クリティカル
- IRRの計算結果（要求リターン20-25%との比較）
- MOICの計算結果（目標2.0倍以上との比較）
- 売却時のEVと株式価値の妥当性
- 年別IRRシミュレーションの評価
- スコア: 0-100点

##### 安全性分析（10%）★クリティカル
- レバレッジレシオの推移（コベナンツ基準との比較）
- インタレストカバレッジレシオの推移（コベナンツ基準との比較）
- DSCRの推移（コベナンツ基準との比較）
- コベナンツ違反リスクの評価
- スコア: 0-100点

##### 感応度分析（5%）
- 買収プレミアムの変化による影響の評価
- 売却倍率の変化による影響の評価
- 売却年度の変化による影響の評価
- スコア: 0-100点

#### 1.2 定性論点（ウェイト合計: 40%）

##### LBO実行可能性（15%）★クリティカル
- キャッシュ創出力の評価
- 収益の安定性の評価
- 成長の可能性の評価
- スコア: 0-100点

##### 負債調達可能性（10%）★クリティカル
- 金融機関との関係の評価
- コベナンツの妥当性の評価
- 負債構成の最適化の評価
- スコア: 0-100点

##### 売却・IPOの展望（8%）★クリティカル
- 売却の展望の評価
- IPOの可能性の評価
- 出口戦略の具体性の評価
- スコア: 0-100点

##### バリュークリエーション計画（7%）
- 業務効率化の余地の評価
- マネジメントチームの評価
- スコア: 0-100点

### 2. 統合評価と実行判断

#### 2.1 総合スコアの算出
$$Total\ Score = \sum_{i=1}^{n} w_i \times score_i$$

ここで：
- $w_i$: 論点$i$のウェイト
- $score_i$: 論点$i$のスコア（0-100点）

#### 2.2 実行判断の基準

##### 実行推奨
- 総合スコア: 75点以上
- IRR: 20%以上
- MOIC: 2.0倍以上
- 安全性指標: コベナンツを満たす見通し
- 定性論点: 主要論点で問題なし

##### 条件付き実行
- 総合スコア: 65-75点
- IRR: 15-20%
- MOIC: 1.5-2.0倍
- 安全性指標: 一部コベナンツに懸念あり
- 定性論点: 一部論点で懸念あり

##### 実行見送り
- 総合スコア: 65点未満
- IRR: 15%未満
- MOIC: 1.5倍未満
- 安全性指標: コベナンツ違反のリスクが高い
- 定性論点: 主要論点で重大な問題あり

### 3. 各論点の評価結果を出力

## 出力形式
JSON形式で以下の構造で出力：
```json
{
  "evaluation_results": {
    "quantitative_points": {
      "lbo_model_building": {
        "score": 0,
        "weight": 0.25,
        "evaluation": "...",
        "details": {
          "leverage_ratio_appropriateness": "...",
          "debt_schedule_appropriateness": "...",
          "financial_statements_accuracy": "..."
        },
        "comments": "..."
      },
      "return_analysis": {
        "score": 0,
        "weight": 0.20,
        "evaluation": "...",
        "details": {
          "irr": 0,
          "irr_vs_required": "...",
          "moic": 0,
          "moic_vs_target": "...",
          "exit_valuation_appropriateness": "...",
          "yearly_irr_simulation": [...]
        },
        "comments": "..."
      },
      "safety_analysis": {
        "score": 0,
        "weight": 0.10,
        "evaluation": "...",
        "details": {
          "leverage_ratio_trend": [...],
          "interest_coverage_trend": [...],
          "dscr_trend": [...],
          "covenant_violation_risk": "..."
        },
        "comments": "..."
      },
      "sensitivity_analysis": {
        "score": 0,
        "weight": 0.05,
        "evaluation": "...",
        "details": {
          "premium_sensitivity": "...",
          "multiple_sensitivity": "...",
          "exit_year_sensitivity": "..."
        },
        "comments": "..."
      }
    },
    "qualitative_points": {
      "lbo_executability": {
        "score": 0,
        "weight": 0.15,
        "evaluation": "...",
        "details": {
          "cash_generation_capability": "...",
          "revenue_stability": "...",
          "growth_potential": "..."
        },
        "comments": "..."
      },
      "debt_financing_feasibility": {
        "score": 0,
        "weight": 0.10,
        "evaluation": "...",
        "details": {
          "financial_institution_relationship": "...",
          "covenant_appropriateness": "...",
          "debt_structure_optimization": "..."
        },
        "comments": "..."
      },
      "exit_prospects": {
        "score": 0,
        "weight": 0.08,
        "evaluation": "...",
        "details": {
          "sale_prospects": "...",
          "ipo_possibility": "...",
          "exit_strategy_specificity": "..."
        },
        "comments": "..."
      },
      "value_creation_plan": {
        "score": 0,
        "weight": 0.07,
        "evaluation": "...",
        "details": {
          "operational_improvement_potential": "...",
          "management_team": "..."
        },
        "comments": "..."
      }
    }
  },
  "total_score": 0,
  "execution_judgment": "実行推奨|条件付き実行|実行見送り",
  "judgment_reasoning": {
    "irr": 0,
    "irr_vs_required": "...",
    "moic": 0,
    "safety_indicators": "...",
    "qualitative_points": "..."
  },
  "key_risks": [
    {
      "risk": "...",
      "severity": "高|中|低",
      "mitigation": "..."
    }
  ],
  "recommended_actions": [
    "..."
  ]
}
```

## 注意事項
- 各論点のスコアは0-100の範囲で算出
- 総合スコアは重み付け平均で算出
- 定量情報と定性情報を統合した結論を明確に示す
- 実行判断は総合スコア、IRR、MOIC、安全性指標、定性論点を総合的に評価して決定
- クリティカル論点（★）の評価結果を重点的に確認
- 参考文献（`dd_logic/references/`）を参照して評価ロジックを適用
- 評価論点（`dd_logic/lbo_dd/evaluation_points/evaluation_points.md`）を参照して評価を実施
