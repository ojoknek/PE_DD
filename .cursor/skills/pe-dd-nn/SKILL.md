---
name: pe-dd-nn
description: Runs NN DD (Non Name Sheet) workflow for PE deals. Loads VDR materials from deals/[deal_name]/vdr/nn/, evaluates using dd_logic criteria, and outputs report to ai_dd_results/nn_dd/. Use when the user asks for NN DD, Non Name evaluation, or processing nn/ materials.
---

# NN DD（Non Name Sheet）

## トリガー
- NN DD、Non Name、vdr/nn の評価・処理を依頼されたとき
- 擬似コマンド: `/nn_dd:init`（初期化）、`/nn_dd:load`（資料読み込み）、`/nn_dd:evaluate`（評価）、`/nn_dd:report`（レポート生成）

## データソース
- **VDR**: `deals/[deal_name]/vdr/nn/`（PDF・URL・Markdown等）

## ワークフロー

### 1. 資料の読み込みと構造化
- `agents/prompts/nn_dd/load_materials_prompt.md` の手順に従う
- 定量・定性を識別し、事業概要・財務・経営陣・市場競合・投資条件をJSONで構造化

### 2. NN DD評価の実行
- 評価基準: `dd_logic/nn_dd/criteria/evaluation_criteria.md`
- 計算ロジック: `dd_logic/nn_dd/calculations/`
- `agents/prompts/nn_dd/evaluate_prompt.md` の手順で各論点を評価し、スコア・推奨を導出

### 3. 結果の出力
- レポートを `deals/[deal_name]/ai_dd_results/nn_dd/report.md` に保存
- 出力フォーマット: `dd_logic/nn_dd/outputs/`

## 参照
- 詳細ワークフロー: `agents/workflows/nn_dd_workflow.md`
- プロンプト詳細: `agents/prompts/nn_dd/` 配下（load_materials_prompt.md, evaluate_prompt.md）
- 評価論点・計算式: `dd_logic/nn_dd/`
- 参考文献: `dd_logic/references/`
