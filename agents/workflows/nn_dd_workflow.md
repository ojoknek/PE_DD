# NN DDワークフロー（Non Name Sheet）

## 概要
Non Name Sheet（NN）を受け取った段階でのNN DDフローです。定量情報と定性情報を統合し、一定の結論を導出します。

## 入力形式
- PDFファイル
- Web情報（URL）
- Markdownファイル（テキスト情報）
- 上記の組み合わせ

## 処理ステップ

### 1. 資料の読み込みと構造化
- 各種形式の資料を読み込み
- 構造化されたデータに変換
- 主要情報の抽出（定量情報・定性情報の識別）

### 2. NN DD評価の実行
- 評価基準に基づく自動評価
- 計算ロジックの適用（定量情報の分析）
- 定性情報の評価
- 定量・定性情報を統合した結論の導出
- 各論点の評価結果の出力

### 3. 結果の出力
- NN DD結果レポートの生成
- 案件ディレクトリへの保存
  - レポート: `deals/[deal_name]/dd_results/nn_dd/report.md`
  - 構造化データ: `deals/[deal_name]/dd_results/nn_dd/data.json`

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
