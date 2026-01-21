# IM DDワークフロー（Information Memorandum）

## 概要
Information Memorandum（IM）をPDFとして受け取った際のIM DDフローです。定量情報と定性情報を統合し、一定の結論を導出します。

## 入力形式
- PDFファイル（Information Memorandum）

## 処理ステップ

### 1. IMの読み込みと解析
- PDFの読み込み
- 構造化されたデータへの変換
- 主要セクションの抽出（定量情報・定性情報の識別）

### 2. IM DD評価の実行
- 評価論点に基づく評価
- 計算ロジックの適用（定量情報の分析）
- 定性情報の評価
- 定量・定性情報を統合した結論の導出
- 各論点の評価結果の出力

### 3. 結果の出力
- IM DD結果レポートの生成
- 案件ディレクトリへの保存
  - レポート: `deals/[deal_name]/dd_results/im_dd/report.md`
  - 構造化データ: `deals/[deal_name]/dd_results/im_dd/data.json`

## 評価論点
詳細は `dd_logic/im_dd/evaluation_points/` を参照

## 計算ロジック
詳細は `dd_logic/im_dd/calculations/` を参照
- 定量情報の分析ロジック
- 定性情報の評価ロジック
- 統合結論導出ロジック

## 出力フォーマット
詳細は `dd_logic/im_dd/outputs/` を参照

## 参考文献
PEファンドDDロジックに関する文献は `dd_logic/references/` を参照
