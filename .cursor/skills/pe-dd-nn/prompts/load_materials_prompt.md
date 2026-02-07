# 資料読み込みプロンプト（NN DD）

## 目的
Non Name Sheet（NN）のVDR資料を読み込み、構造化されたデータに変換します。定量情報と定性情報を識別して分類します。

## 入力
- VDR資料（`deals/[deal_name]/vdr/nn/` 配下のPDFファイル、Web情報（URL）、Markdownファイル等）

## 処理手順
1. 各種形式の資料を読み込む
2. 主要情報を抽出する（定量情報・定性情報を識別）：
   - 事業概要（定量・定性）
   - 財務情報（定量）
   - 経営陣・組織情報（定性）
   - 市場・競合情報（定量・定性）
   - 投資条件（定量）
3. 構造化されたデータに変換する（定量・定性情報の分類を含む）

## 出力形式
JSON形式で以下の構造で出力：
```json
{
  "business_overview": {
    "business_description": "...",
    "business_model": "...",
    "market_size": "...",
    "market_growth": "..."
  },
  "financial_info": {
    "revenue": 0,
    "growth_rate": 0,
    "ebitda": 0,
    "operating_income": 0,
    "net_income": 0,
    "equity": 0,
    "total_assets": 0
  },
  "management_team": {
    "management_experience": 0,
    "organization_structure": "...",
    "team_size": 0
  },
  "market_competition": {
    "market_position": "...",
    "competitive_advantage": "...",
    "market_growth": 0
  },
  "investment_terms": {
    "investment_amount": 0,
    "valuation": 0,
    "investment_period": 0,
    "exit_strategy": "..."
  }
}
```

## 注意事項
- 数値データは適切な単位で記録する
- 不明な情報は null または空文字列とする
- 抽出した情報の出典を記録する
- 定量情報と定性情報を明確に分類する
- 定量情報には数値データ、定性情報にはテキストデータを記録する
