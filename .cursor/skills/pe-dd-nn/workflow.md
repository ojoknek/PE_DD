# NN DDワークフロー（Non Name Sheet）

## 概要
Non Name Sheet（NN）を受け取った段階でのNN DDフローです。定量情報と定性情報を統合し、一定の結論を導出します。

## データソース

NN DD評価に必要なデータは、以下のディレクトリから取得します：
- **VDR資料**: `deals/[deal_name]/vdr/nn/` - NN関連VDR資料（必須）
- **財務諸表**: VDR資料から抽出した財務諸表データ
- **事業情報**: VDR資料から抽出した事業情報データ

## 入力形式
- VDR資料（PDFファイル、Web情報（URL）、Markdownファイル等、`deals/[deal_name]/vdr/nn/` 配下）

## 処理ステップ

### 1. 資料の読み込みと構造化
- VDR資料の読み込み（`.cursor/skills/pe-dd-nn/prompts/load_materials_prompt.md` を使用）
- 各種形式の資料を読み込み
- 構造化されたデータに変換
- 主要情報の抽出（定量情報・定性情報の識別）

### 2. NN DD評価の実行
- NN DD評価の実行（`.cursor/skills/pe-dd-nn/prompts/evaluate_prompt.md` を使用）
- 評価基準に基づく自動評価
- 計算ロジックの適用（定量情報の分析）
- 定性情報の評価
- 定量・定性情報を統合した結論の導出
- 各論点の評価結果の出力

### 3. 結果の出力
- NN DD結果レポートの生成
- 案件ディレクトリへの保存
  - レポート: `deals/[deal_name]/ai_dd_results/nn_dd/report.md`

## 評価論点
詳細は `dd_logic/nn_dd/criteria/` を参照

## 計算ロジック
詳細は `dd_logic/nn_dd/calculations/` を参照
- 定量情報の分析ロジック
- 定性情報の評価ロジック
- 統合結論導出ロジック

## 出力フォーマット
詳細は `dd_logic/nn_dd/outputs/` を参照

## 参考文献
PEファンドDDロジックに関する文献は `dd_logic/references/` を参照
