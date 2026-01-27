# LBOモデル構築プロンプト

## 目的
構造化されたVDRデータを基に、LBOモデルを構築します。参考文献「壁の道の向こう側」の投資銀行の本格的LBOモデル作成方法（18ステップ）に基づいて、財務3表を構築し、レバレッジ、負債スケジュール、IRR、MOIC等を計算します。

## 入力
- 構造化されたVDRデータ（JSON形式、`load_vdr_prompt.md`の出力）
- LBOモデル構築の数式仕様書（`dd_logic/lbo_dd/calculations/lbo_model.md`を参照）
- DCF分析の数式仕様書（`dd_logic/lbo_dd/calculations/dcf_analysis.md`を参照）

## 処理手順

### 1. LBOモデル構築の18ステップを実行

#### ステップ1-11: 基本オペレーティングモデルの構築
1. エクセルの反復計算をオフにする（概念的に）
2. 損益計算書（IS）を構築する（減価償却、受取・支払利息は空欄のまま）
3. 設備投資や資本等（mixed account）と運転資本を計算し、減価償却をISにリンクさせる
4. 負債の返済スケジュールと受取・支払利息を計算する（手数料と償却スケジュールの設定）
5. 貸借対照表（BS）を構築する（現金と短期借入金は除く）
6. BSの各項目をキャッシュフロー計算書（CF）の項目毎に分類する
7. CFを構築する（**EBITDAベースで営業CFを構築**）
8. CFで算出した現金/短期借入金をBSにリンクさせる
9. 受取・支払利息をISにリンクさせる（循環参照発生）
10. エクセルの反復計算をオンにする（概念的に）
11. 循環参照のオン・オフができるスイッチを構築する（概念的に）

#### ステップ12-15: キャッシュスイープモデルの構築
12. 期末の負債残高をBSにリンクさせ、BSの負債残高前年比をCFにリンクさせる
13. キャッシュスイープのついた負債の返済スケジュールと受取・支払利息を計算する
14. 期末の負債残高をBSにリンクさせ、BSの負債残高前年比をCFにリンクさせる
15. 受取・支払利息をISにリンクさせる（循環参照発生）

#### ステップ16-18: 分析と評価
16. 安全性分析を行う
17. 売却時のEnterprise value（EV）と株式価値を計算する
18. 収益率と感応度の分析を行う

### 2. 主要計算項目の実行

#### 2.1 レバレッジ比率の設定
- 買収価格の算定: $Purchase\ Price = Equity\ Value + Net\ Debt$
- エクイティ・コントリビューションの計算: $Equity\ Contribution = Purchase\ Price - Total\ Debt$
- レバレッジ比率の計算: $Leverage\ Ratio = \frac{Total\ Debt}{Equity\ Contribution}$

#### 2.2 負債スケジュールの構築（キャッシュスイープ付き）
- 各年度の負債残高: $Debt\ Balance_{t} = Debt\ Balance_{t-1} - Scheduled\ Repayment_t - Cash\ Sweep_t$
- 利用可能現金: $Available\ Cash_{t} = Beginning\ Cash_{t} + Operating\ CF_{t} - Minimum\ Cash_{t}$
- キャッシュスイープ: $Cash\ Sweep_{t} = \min(Available\ Cash_{t}, Remaining\ Debt_{t})$
- 支払利息の計算（固定金利・変動金利）

#### 2.3 IRR（内部収益率）の計算
- IRRの定義: $\sum_{t=0}^{n} \frac{CF_t}{(1 + IRR)^t} = 0$
- 年別IRRシミュレーション: $IRR_t = \left(\frac{Exit\ Equity\ Value_t}{Equity\ Contribution}\right)^{\frac{1}{t}} - 1$

#### 2.4 MOIC（Multiple of Invested Capital）の計算
- MOICの定義: $MOIC = \frac{Exit\ Equity\ Value}{Equity\ Contribution}$
- MOICとIRRの関係: $MOIC = (1 + IRR)^n$

#### 2.5 安全性分析
- レバレッジレシオ: $Leverage\ Ratio = \frac{Total\ Debt}{EBITDA}$
- インタレストカバレッジレシオ: $Interest\ Coverage\ Ratio = \frac{EBIT}{Interest\ Expense}$
- DSCR: $DSCR = \frac{EBITDA}{Interest\ Expense + Principal\ Repayment}$
- コベナンツ（財務制限条項）のチェック

#### 2.6 売却時のEVと株式価値の計算
- 売却時のEV: $Exit\ EV = Exit\ EBITDA \times EV/EBITDA\ Multiple$
- 売却時の株式価値: $Exit\ Equity\ Value = Exit\ EV - Exit\ Net\ Debt + Non\ Operating\ Assets - Minority\ Interest$
- PEファンドの持分比率を考慮: $PE\ Fund\ Exit\ Value = Exit\ Equity\ Value \times Ownership\ Percentage$

#### 2.7 感応度分析
- 買収プレミアムの変化による影響
- 売却倍率の変化による影響
- 売却年度の変化による影響

## 出力形式
JSON形式で以下の構造で出力：
```json
{
  "lbo_model": {
    "acquisition_terms": {
      "purchase_price": 0,
      "equity_contribution": 0,
      "total_debt": 0,
      "leverage_ratio": 0
    },
    "debt_schedule": [
      {
        "year": "YYYY",
        "term_loan_a": {
          "beginning_balance": 0,
          "scheduled_repayment": 0,
          "cash_sweep": 0,
          "interest_payment": 0,
          "ending_balance": 0
        },
        "term_loan_b": {
          "beginning_balance": 0,
          "scheduled_repayment": 0,
          "cash_sweep": 0,
          "interest_payment": 0,
          "ending_balance": 0
        },
        "high_yield_bond": {
          "beginning_balance": 0,
          "scheduled_repayment": 0,
          "cash_sweep": 0,
          "interest_payment": 0,
          "ending_balance": 0
        },
        "total_debt": 0,
        "total_interest": 0
      }
    ],
    "cash_flow": [
      {
        "year": "YYYY",
        "ebitda": 0,
        "operating_cf": 0,
        "available_cash": 0,
        "minimum_cash": 0,
        "cash_sweep": 0
      }
    ],
    "returns": {
      "irr": 0,
      "moic": 0,
      "yearly_irr": [
        {
          "exit_year": 0,
          "irr": 0,
          "moic": 0,
          "exit_equity_value": 0
        }
      ]
    },
    "safety_analysis": [
      {
        "year": "YYYY",
        "leverage_ratio": 0,
        "interest_coverage_ratio": 0,
        "dscr": 0,
        "covenant_compliance": {
          "max_leverage_ok": true,
          "min_interest_coverage_ok": true,
          "min_dscr_ok": true
        }
      }
    ],
    "exit_valuation": {
      "exit_ebitda": 0,
      "exit_ev_ebitda_multiple": 0,
      "exit_ev": 0,
      "exit_net_debt": 0,
      "exit_equity_value": 0,
      "pe_fund_ownership": 0,
      "pe_fund_exit_value": 0
    },
    "sensitivity_analysis": {
      "premium_sensitivity": [
        {
          "premium": 0,
          "purchase_price": 0,
          "irr": 0,
          "moic": 0
        }
      ],
      "multiple_sensitivity": [
        {
          "exit_multiple": 0,
          "exit_ev": 0,
          "irr": 0,
          "moic": 0
        }
      ],
      "exit_year_sensitivity": [
        {
          "exit_year": 0,
          "irr": 0,
          "moic": 0
        }
      ]
    }
  }
}
```

## 注意事項
- 数式仕様書（`dd_logic/lbo_dd/calculations/lbo_model.md`）を参照して、適切な計算式を適用する
- 18ステップの構築プロセスを順序通りに実行する
- EBITDAベースで営業CFを構築する（支払利息をCF上で表示するため）
- キャッシュスイープは負債返済の優先順位（タームローンA → タームローンB → ハイイールド債）に従う
- ミニマムキャッシュを適切に設定する
- 循環参照を適切に処理する（概念的に）
- 各年度の安全性指標を計算し、コベナンツ違反リスクを評価する
- 感応度分析は複数の変数を組み合わせて実施する
