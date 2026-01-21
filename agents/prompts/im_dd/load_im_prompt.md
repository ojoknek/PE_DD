# IM読み込みプロンプト

## 目的
Information Memorandum（IM）をPDF形式で読み込み、構造化されたデータに変換します。

## 入力
- PDFファイル（Information Memorandum）

## 処理手順
1. PDFファイルを読み込む
2. 主要セクションを抽出する（定量情報・定性情報を識別）：
   - エグゼクティブサマリー（定性）
   - 事業概要（定量・定性）
   - 財務情報（定量）
   - 経営陣情報（定性）
   - 市場・競合情報（定量・定性）
   - 投資条件（定量）
3. 構造化されたデータに変換する（定量・定性情報の分類を含む）

## 出力形式
JSON形式で以下の構造で出力：
```json
{
  "executive_summary": "...",
  "business_overview": {
    "business_description": "...",
    "business_model": "...",
    "market_position": "...",
    "growth_strategy": "..."
  },
  "financial_info": {
    "financial_statements": {...},
    "profitability": {...},
    "financial_health": {...},
    "forecasts": {...}
  },
  "management_team": {
    "management_capability": "...",
    "organization_structure": "...",
    "governance": "..."
  },
  "market_competition": {
    "market_analysis": "...",
    "competitive_analysis": "...",
    "market_risks": "..."
  },
  "investment_terms": {
    "valuation": {...},
    "investment_conditions": {...},
    "exit_strategy": "..."
  }
}
```

## 注意事項
- PDFの構造に応じて適切にセクションを識別する
- 数値データは適切な単位で記録する
- 不明な情報は null または空文字列とする
- 定量情報と定性情報を明確に分類する
- 定量情報には数値データ、定性情報にはテキストデータを記録する