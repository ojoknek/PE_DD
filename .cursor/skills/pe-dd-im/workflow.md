# IM DDワークフロー（Information Memorandum）

## 概要
Information Memorandum（IM）を基にしたIM DDフローです。定量情報と定性情報を統合し、一定の結論を導出します。

## データソース

IM DD評価に必要なデータは、以下のディレクトリから取得します：
- **VDR資料**: `deals/[deal_name]/vdr/im/` - IM関連VDR資料（必須）
- **財務諸表**: VDR資料から抽出した財務諸表データ
- **事業計画**: VDR資料から抽出した事業計画データ

## 入力形式
- VDR資料（PDFファイル等、`deals/[deal_name]/vdr/im/` 配下）

## 実行前: PDF→PNG変換
- **IM DD の処理ステップを開始する前に**、当該案件の `vdr/im/` 内のPDFについて、同じフォルダに `{PDFのベース名}_page0001.png` が無ければ未変換とみなす
- 未変換のPDFには **`/program` 配下の venv で** PDF→PNG を実行する: `program/venv/bin/python program/pdf_table_extractor.py <PDFパス> --ensure`
- 変換完了後に IM の読み込み・評価に進む

## 処理ステップ

### 1. IMの読み込みと解析
- VDR資料の読み込み（`.cursor/skills/pe-dd-im/prompts/load_im_prompt.md` を使用）
- 構造化されたデータへの変換
- 主要セクションの抽出（定量情報・定性情報の識別）

### 2. IM DD評価の実行
- IM DD評価の実行（`.cursor/skills/pe-dd-im/prompts/evaluate_prompt.md` を使用）
- 評価論点に基づく評価
- 計算ロジックの適用（定量情報の分析）
- 定性情報の評価
- 定量・定性情報を統合した結論の導出
- 各論点の評価結果の出力

### 3. 結果の出力
- IM DD結果レポートの生成
- 案件ディレクトリへの保存
  - レポート: `deals/[deal_name]/ai_dd_results/im_dd/report.md`

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
