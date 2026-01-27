# Information Memorandum（IM）関連資料

## 概要
Information Memorandum（IM）を基にしたIM DDの入力資料を管理するディレクトリです。IM資料を基にしたIM DD評価の入力として使用されます。

## 使用方法

### 1. 資料の配置
IM関連VDR資料（PDF）をこのディレクトリに配置します。

### 2. ワークフローの実行
IM DDワークフローを実行します。
- 詳細な手順: `agents/workflows/im_dd_workflow.md` を参照
- AI/LLMを使用したプロンプトベースで実装
- 計算ロジックは数式仕様書（`dd_logic/im_dd/calculations/`）を参照

### 3. 結果の確認
- **DD結果**: `../../ai_dd_results/im_dd/` に自動生成されます
  - `report.md`: IM DD結果レポート（人間が読みやすい形式）

## 評価内容
IM DDでは以下の評価が実施されます：
- 定量情報と定性情報を統合した評価
- 事業性評価、財務評価、経営陣評価、リスク評価、投資条件評価の各論点の評価
- DCF分析、バリュエーション分析、リスク分析の実施
- 総合スコアと投資推奨度の算出

詳細は `dd_logic/im_dd/evaluation_points/` を参照してください。

## 関連ディレクトリ
- **DD結果**: `../../ai_dd_results/im_dd/` - IM DD評価結果
- **評価ロジック**: `dd_logic/im_dd/` - IM DD評価ロジック
- **ワークフロー定義**: `agents/workflows/im_dd_workflow.md` - IM DDワークフロー