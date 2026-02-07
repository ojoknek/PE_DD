---
name: pe-dd-lbo
description: Runs LBO DD workflow for PE deals. Loads VDR from deals/[deal_name]/vdr/im/, builds LBO model (18-step, cash sweep, IRR/MOIC), evaluates execution judgment, and outputs report to ai_dd_results/lbo_dd/. Use when the user asks for LBO DD, LBO model, leverage buyout, IRR/MOIC, or execution judgment.
---

# LBO DD（Leveraged Buyout）

## トリガー
- LBO DD、LBOモデル構築、実行判断の評価を依頼されたとき
- 擬似コマンド: `/lbo_dd:init`（初期化）、`/lbo_dd:build_model`（モデル構築）、`/lbo_dd:calculate`（LBO計算）、`/lbo_dd:evaluate`（実行判断）、`/lbo_dd:report`（レポート生成）

## データソース
- **VDR**: `deals/[deal_name]/vdr/im/`（財務諸表・事業計画・買収条件・負債調達情報）

## ワークフロー

### 1. VDR資料の読み込みと構造化
- `agents/prompts/lbo_dd/load_vdr_prompt.md` の手順に従う
- 財務3表（IS/BS/CF）・事業計画・買収条件・負債構成・コベナンツをJSONで構造化

### 2. LBOモデルの構築
- `agents/prompts/lbo_dd/build_lbo_model_prompt.md` の18ステップに従う
- 数式仕様: `dd_logic/lbo_dd/calculations/`（lbo_model, dcf_analysis）
- レバレッジ・負債スケジュール（キャッシュスイープ）・IRR・MOIC・安全性分析・感応度を算出

### 3. LBO DD評価と実行判断
- 評価論点: `dd_logic/lbo_dd/evaluation_points/evaluation_points.md`
- `agents/prompts/lbo_dd/evaluate_lbo_prompt.md` の手順で定量・定性を評価
- 実行判断: **実行推奨**（スコア75+、IRR≥20%、MOIC≥2.0） / **条件付き実行** / **実行見送り**

### 4. 結果の出力
- レポートを `deals/[deal_name]/ai_dd_results/lbo_dd/report.md` に保存
- テンプレート: `dd_logic/lbo_dd/outputs/report_template.md`

## 参照
- 詳細ワークフロー: `agents/workflows/lbo_dd_workflow.md`
- プロンプト詳細: `agents/prompts/lbo_dd/` 配下（load_vdr_prompt.md, build_lbo_model_prompt.md, evaluate_lbo_prompt.md）
- 評価論点・計算式: `dd_logic/lbo_dd/`
- 参考文献: `dd_logic/references/`
