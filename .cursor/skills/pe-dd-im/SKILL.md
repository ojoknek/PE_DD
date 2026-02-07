---
name: pe-dd-im
description: Runs IM DD (Information Memorandum) workflow for PE deals. Loads IM from deals/[deal_name]/vdr/im/, evaluates using dd_logic evaluation points and DCF, and outputs report to ai_dd_results/im_dd/. Use when the user asks for IM DD, Information Memorandum evaluation, or processing im/ materials.
---

# IM DD（Information Memorandum）

## トリガー
- IM DD、Information Memorandum、vdr/im の評価・処理を依頼されたとき
- 擬似コマンド: `/im_dd:init`（初期化）、`/im_dd:load_im`（IM読み込み）、`/im_dd:evaluate`（評価）、`/im_dd:report`（レポート生成）

## データソース
- **VDR**: `deals/[deal_name]/vdr/im/`（PDF等）

## ワークフロー

### 1. IMの読み込みと解析
- `.cursor/skills/pe-dd-im/prompts/load_im_prompt.md` の手順に従う
- エグゼクティブサマリー・事業概要・財務・経営陣・市場競合・投資条件をJSONで構造化

### 2. IM DD評価の実行
- 評価論点: `dd_logic/im_dd/evaluation_points/evaluation_points.md`
- 計算ロジック（DCF等）: `dd_logic/im_dd/calculations/`
- `.cursor/skills/pe-dd-im/prompts/evaluate_prompt.md` の手順で各論点を評価し、投資推奨度を導出

### 3. 結果の出力
- レポートを `deals/[deal_name]/ai_dd_results/im_dd/report.md` に保存
- 出力フォーマット: `dd_logic/im_dd/outputs/`

## 参照
- 詳細ワークフロー: `.cursor/skills/pe-dd-im/workflow.md`
- プロンプト詳細: `.cursor/skills/pe-dd-im/prompts/` 配下（load_im_prompt.md, evaluate_prompt.md）
- 評価論点・計算式: `dd_logic/im_dd/`
- 参考文献: `dd_logic/references/`
