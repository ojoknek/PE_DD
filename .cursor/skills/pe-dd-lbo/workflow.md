# LBO DDワークフロー（Leveraged Buyout）

## 概要
LBO（Leveraged Buyout）モデルを構築し、実行判断にかかる意思決定を支援するLBO DDフローです。VDR資料を基にLBOモデルを構築し、定量・定性情報を統合して実行判断を導出します。

## データソース

- **VDR資料**: `deals/[deal_name]/vdr/im/` - IM関連VDR資料（必須）
- **財務諸表・事業計画**: VDR資料から抽出

## 処理ステップ

### 1. VDR資料の読み込みと構造化
- VDR資料の読み込み（`.cursor/skills/pe-dd-lbo/prompts/load_vdr_prompt.md` を使用）
- 財務諸表・事業計画・買収条件・負債調達情報の抽出とJSON化

### 2. LBOモデルの構築
- LBOモデル構築の実行（`.cursor/skills/pe-dd-lbo/prompts/build_lbo_model_prompt.md` を使用）
- 18ステップの構築プロセス、レバレッジ・負債スケジュール（キャッシュスイープ）・IRR・MOIC・安全性分析・売却時EV・感応度分析

### 3. LBO DD評価の実行
- LBO DD評価の実行（`.cursor/skills/pe-dd-lbo/prompts/evaluate_lbo_prompt.md` を使用）
- 定量論点（60%）・定性論点（40%）の評価、総合スコア、実行判断（実行推奨/条件付き実行/実行見送り）の導出

### 4. 結果の出力
- レポート: `deals/[deal_name]/ai_dd_results/lbo_dd/report.md`
- テンプレート: `dd_logic/lbo_dd/outputs/report_template.md`

## 評価論点・計算ロジック
- `dd_logic/lbo_dd/evaluation_points/evaluation_points.md`
- `dd_logic/lbo_dd/calculations/`（lbo_model.md, dcf_analysis.md）

## 実行判断の基準
- **実行推奨**: 総合75点以上、IRR≥20%、MOIC≥2.0、コベナンツ満たす見通し
- **条件付き実行**: 65-75点、IRR 15-20%、MOIC 1.5-2.0
- **実行見送り**: 65点未満、IRR<15%、MOIC<1.5、コベナンツ違反リスク高

## 参考文献
`dd_logic/references/` を参照
