# NN DD用プロンプト

## 概要
Non Name Sheet（NN）を受け取った段階でのNN DD用プロンプト集です。定量情報と定性情報を統合した結論導出を支援します。

## プロンプト一覧

### 1. 資料読み込みプロンプト
- **ファイル**: `load_materials_prompt.md`
- **用途**: 各種形式（PDF/Web/md）の資料を読み込み、構造化するためのプロンプト
- **機能**: 定量情報と定性情報の識別

### 2. NN DD評価プロンプト
- **ファイル**: `evaluate_prompt.md`
- **用途**: 評価基準に基づいてNN DD評価を実行するためのプロンプト
- **機能**:
  - 定量情報と定性情報を統合した結論導出
  - 計算ロジックは数式仕様書（`dd_logic/nn_dd/calculations/`）を参照
  - 評価基準は `dd_logic/nn_dd/criteria/evaluation_criteria.md` を参照

### 3. 結果出力プロンプト
- **用途**: NN DD結果をレポート形式で出力するためのプロンプト
- **出力先**: `deals/[deal_name]/ai_dd_results/nn_dd/report.md`

## データソース

NN DD評価に必要なデータは、以下のディレクトリから取得します：
- **VDR資料**: `deals/[deal_name]/vdr/nn/` - NN関連VDR資料（必須）

## 使用方法
各プロンプトは、本スキル配下の `workflow.md` のステップで使用されます。計算ロジックは数式仕様書を参照して、適切な計算式を適用してください。

## 関連ドキュメント
- **評価基準**: `dd_logic/nn_dd/criteria/evaluation_criteria.md`
- **計算ロジック**: `dd_logic/nn_dd/calculations/`
- **ワークフロー**: 本スキル配下の `workflow.md`
