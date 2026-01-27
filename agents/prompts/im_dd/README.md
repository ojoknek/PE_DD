# IM DD用プロンプト

## 概要
Information Memorandum（IM）を基にしたIM DD用プロンプト集です。定量情報と定性情報を統合した結論導出を支援します。

## プロンプト一覧

### 1. IM読み込みプロンプト
- **ファイル**: `load_im_prompt.md`
- **用途**: PDF形式のIMを読み込み、構造化するためのプロンプト
- **機能**: 定量情報と定性情報の識別

### 2. IM DD評価プロンプト
- **ファイル**: `evaluate_prompt.md`
- **用途**: 評価論点に基づいてIM DD評価を実行するためのプロンプト
- **機能**: 
  - 定量情報と定性情報を統合した結論導出
  - 計算ロジックは数式仕様書（`dd_logic/im_dd/calculations/`）を参照
  - DCF分析は `dd_logic/im_dd/calculations/dcf_analysis.md` を参照
  - 評価論点は `dd_logic/im_dd/evaluation_points/evaluation_points.md` を参照

### 3. 結果出力プロンプト
- **用途**: IM DD結果をレポート形式で出力するためのプロンプト
- **出力先**: `deals/[deal_name]/ai_dd_results/im_dd/report.md`

## データソース

IM DD評価に必要なデータは、以下のディレクトリから取得します：
- **VDR資料**: `deals/[deal_name]/vdr/im/` - IM関連VDR資料（必須）

## 使用方法
各プロンプトは、対応するワークフローのステップで使用されます。計算ロジックは数式仕様書を参照して、適切な計算式を適用してください。

## 関連ドキュメント
- **評価論点**: `dd_logic/im_dd/evaluation_points/evaluation_points.md`
- **計算ロジック**: `dd_logic/im_dd/calculations/`
- **ワークフロー**: `agents/workflows/im_dd_workflow.md`
