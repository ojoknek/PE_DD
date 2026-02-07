# VDR資料読み込みプロンプト（LBO DD）

## 目的
LBO DD評価に必要なVDR資料を読み込み、構造化されたデータに変換します。特にLBOモデル構築に必要な財務諸表データと事業計画データを抽出します。

## 入力
- VDR資料（`deals/[deal_name]/vdr/im/` 配下のPDFファイル等）
- 財務諸表データ（損益計算書、貸借対照表、キャッシュフロー計算書）
- 事業計画データ

## 処理手順
1. VDR資料を読み込む
2. 主要セクションを抽出する（LBOモデル構築に必要な情報を識別）：
   - **財務諸表情報（定量）**:
     - 損益計算書（IS）: 売上高、EBITDA、EBIT、減価償却、支払利息等
     - 貸借対照表（BS）: 資産、負債、資本等
     - キャッシュフロー計算書（CF）: 営業CF、投資CF、財務CF等
     - 過去実績データ（最低3-5年分）
   - **事業計画情報（定量・定性）**:
     - 将来計画（売上高、EBITDA、EBIT等の予測）
     - 設備投資計画（Capex）
     - 運転資本の見通し
     - 事業戦略（定性）
   - **買収条件情報（定量）**:
     - 買収価格（株式価値）
     - 既存負債（Net Debt）
     - 買収時のEV/EBITDA倍率
   - **負債調達情報（定量）**:
     - 負債構成（タームローンA/B、ハイイールド債等）
     - 金利条件（固定金利・変動金利）
     - 返済スケジュール
     - コベナンツ（財務制限条項）

3. 構造化されたデータに変換する（定量・定性情報の分類を含む）

## 出力形式
JSON形式で以下の構造で出力：
- `financial_statements`: income_statement, balance_sheet, cash_flow_statement（historical / forecast）
- `business_plan`: growth_strategy, capex_plan, working_capital_assumptions
- `acquisition_terms`: purchase_price, equity_value, net_debt, ev_ebitda_multiple
- `debt_structure`: total_debt, term_loan_a/b, high_yield_bond, covenants（max_leverage_ratio, min_interest_coverage, min_dscr）
- `exit_assumptions`: exit_year, exit_ebitda_multiple, ownership_percentage

## 注意事項
- PDFの構造に応じて適切にセクションを識別する
- 数値データは適切な単位（百万円等）で記録する
- 不明な情報は null または空文字列とする
- LBOモデル構築に必要な全ての情報を抽出する
- 過去実績データは最低3-5年分を確保する
- 将来計画データは投資期間（通常3-5年）分を確保する
