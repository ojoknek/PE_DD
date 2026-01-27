# Non Name Sheet（NN）関連資料

## 概要
Non Name Sheet（NN）を受け取った段階での入力資料を管理するディレクトリです。NN資料を基にしたNN DD評価の入力として使用されます。

## 使用方法

### 1. 資料の配置
NN関連VDR資料をこのディレクトリに配置します。
- PDFファイル
- Web情報（URL）
- Markdownファイル（テキスト情報）
- 上記の組み合わせ

### 2. ワークフローの実行
NN DDワークフローを実行します。
- 詳細な手順: `agents/workflows/nn_dd_workflow.md` を参照
- AI/LLMを使用したプロンプトベースで実装
- 計算ロジックは数式仕様書（`dd_logic/nn_dd/calculations/`）を参照

### 3. 結果の確認
- **DD結果**: `../../ai_dd_results/nn_dd/` に自動生成されます
  - `report.md`: NN DD結果レポート（人間が読みやすい形式）

## 評価内容
NN DDでは以下の評価が実施されます：
- 定量情報と定性情報を統合した評価
- 事業概要、財務情報、経営陣・組織、市場・競合、投資条件の各論点の評価
- 総合スコアとリスクスコアの算出
- 投資推奨度の判定

詳細は `dd_logic/nn_dd/criteria/` を参照してください。

## 関連ディレクトリ
- **DD結果**: `../../ai_dd_results/nn_dd/` - NN DD評価結果
- **評価ロジック**: `dd_logic/nn_dd/` - NN DD評価ロジック
- **ワークフロー定義**: `agents/workflows/nn_dd_workflow.md` - NN DDワークフロー