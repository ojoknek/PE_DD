# LBO DD評価プロンプト

## 目的
構築されたLBOモデルを基に、LBO DD評価を実行します。定量情報と定性情報を統合し、実行判断（実行推奨/条件付き実行/実行見送り）を導出します。

## 入力
- 構築されたLBOモデル（JSON形式、`build_lbo_model_prompt.md`の出力）
- 構造化されたVDRデータ（JSON形式、`load_vdr_prompt.md`の出力）
- 評価論点（`dd_logic/lbo_dd/evaluation_points/evaluation_points.md`を参照）

## 処理手順

### 1. 各評価論点について評価を実行

#### 定量論点（60%）
- LBOモデル構築（25%）★、リターン分析（20%）★、安全性分析（10%）★、感応度分析（5%）

#### 定性論点（40%）
- LBO実行可能性（15%）★、負債調達可能性（10%）★、売却・IPOの展望（8%）★、バリュークリエーション計画（7%）

### 2. 統合評価と実行判断

- 総合スコア: 重み付け平均
- **実行推奨**: 総合75点以上、IRR≥20%、MOIC≥2.0、コベナンツ満たす見通し
- **条件付き実行**: 65-75点、IRR 15-20%、MOIC 1.5-2.0、一部懸念あり
- **実行見送り**: 65点未満、IRR<15%、MOIC<1.5、コベナンツ違反リスク高

### 3. 各論点の評価結果を出力

## 出力形式
JSON形式で evaluation_results（quantitative_points, qualitative_points）, total_score, execution_judgment, judgment_reasoning, key_risks, recommended_actions を出力。詳細は `dd_logic/lbo_dd/evaluation_points/evaluation_points.md` を参照。

## 注意事項
- 各論点のスコアは0-100の範囲で算出
- 実行判断は総合スコア・IRR・MOIC・安全性・定性を総合して決定
- クリティカル論点（★）の評価結果を重点確認
