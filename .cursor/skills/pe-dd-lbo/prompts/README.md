# LBO DD用プロンプト

## 概要
LBO（Leveraged Buyout）モデルを基にしたLBO DD用プロンプト集です。LBOローンモデルを構築し、実行判断にかかる意思決定を支援します。

## データソース

- **VDR資料**: `deals/[deal_name]/vdr/im/` - IM関連VDR資料（必須）
- **財務諸表・事業計画**: VDR資料から抽出

## プロンプト一覧

### 1. VDR資料読み込みプロンプト
- **ファイル**: `load_vdr_prompt.md`
- **用途**: VDR資料を読み込み、LBOモデル構築に必要な情報を構造化する

### 2. LBOモデル構築プロンプト
- **ファイル**: `build_lbo_model_prompt.md`
- **用途**: 構造化されたVDRデータを基にLBOモデルを構築（18ステップ）
- **計算ロジック**: `dd_logic/lbo_dd/calculations/`（lbo_model.md, dcf_analysis.md）

### 3. LBO DD評価プロンプト
- **ファイル**: `evaluate_lbo_prompt.md`
- **用途**: 構築されたLBOモデルを基にLBO DD評価・実行判断を導出
- **評価論点**: `dd_logic/lbo_dd/evaluation_points/evaluation_points.md`

### 4. 結果出力
- **出力先**: `deals/[deal_name]/ai_dd_results/lbo_dd/report.md`
- **テンプレート**: `dd_logic/lbo_dd/outputs/report_template.md`

## 使用方法
各プロンプトは、本スキル配下の `workflow.md` のステップで使用されます。

## 関連ドキュメント
- **評価論点**: `dd_logic/lbo_dd/evaluation_points/evaluation_points.md`
- **計算ロジック**: `dd_logic/lbo_dd/calculations/`
- **ワークフロー**: 本スキル配下の `workflow.md`
