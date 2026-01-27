# LBO DD用プロンプト

## 概要
LBO（Leveraged Buyout）モデルを基にしたLBO DD用プロンプト集です。LBOローンモデルを構築し、実行判断にかかる意思決定を支援します。定量情報と定性情報を統合した結論導出を支援します。

## データソース

LBO DD評価に必要なデータは、以下のディレクトリから取得します：
- **VDR資料**: `deals/[deal_name]/vdr/im/` - IM関連VDR資料（必須）
- **財務諸表**: VDR資料から抽出した財務諸表データ
- **事業計画**: VDR資料から抽出した事業計画データ

## プロンプト一覧

### 1. VDR資料読み込みプロンプト
- **ファイル**: `load_vdr_prompt.md`
- **用途**: VDR資料を読み込み、LBOモデル構築に必要な情報を構造化するためのプロンプト
- **機能**: 
  - 財務諸表データの抽出（損益計算書、貸借対照表、キャッシュフロー計算書）
  - 事業計画データの抽出
  - 買収条件情報の抽出
  - 負債調達情報の抽出
  - 定量情報と定性情報の識別

### 2. LBOモデル構築プロンプト
- **ファイル**: `build_lbo_model_prompt.md`
- **用途**: 構造化されたVDRデータを基に、LBOモデルを構築するためのプロンプト
- **機能**: 
  - LBOモデル構築の18ステップを実行
  - レバレッジ比率の設定
  - 負債スケジュールの構築（キャッシュスイープ付き）
  - IRR（内部収益率）の計算
  - MOIC（Multiple of Invested Capital）の計算
  - 安全性分析（レバレッジレシオ、インタレストカバレッジレシオ、DSCR）
  - 売却時のEVと株式価値の計算
  - 感応度分析
  - 計算ロジックは数式仕様書（`dd_logic/lbo_dd/calculations/`）を参照
    - `lbo_model.md`: LBOモデル構築の数式仕様書
    - `dcf_analysis.md`: DCF分析の数式仕様書

### 3. LBO DD評価プロンプト
- **ファイル**: `evaluate_lbo_prompt.md`
- **用途**: 構築されたLBOモデルを基に、LBO DD評価を実行するためのプロンプト
- **機能**: 
  - 定量情報と定性情報を統合した結論導出
  - 各評価論点の評価（定量論点60%、定性論点40%）
  - 総合スコアの算出
  - 実行判断（実行推奨/条件付き実行/実行見送り）の導出
  - 評価論点は `dd_logic/lbo_dd/evaluation_points/evaluation_points.md` を参照

### 4. 結果出力プロンプト
- **用途**: LBO DD結果をレポート形式で出力するためのプロンプト
- **出力先**: `deals/[deal_name]/ai_dd_results/lbo_dd/report.md`
- **出力内容**:
  - LBOモデル構築結果
  - リターン分析（IRR、MOIC）
  - 安全性分析
  - 感応度分析
  - 各論点の評価結果
  - 実行判断と推奨アクション

## 使用方法
各プロンプトは、対応するワークフローのステップで使用されます。計算ロジックは数式仕様書を参照して、適切な計算式を適用してください。

## 関連ドキュメント
- **評価論点**: `dd_logic/lbo_dd/evaluation_points/evaluation_points.md`
- **計算ロジック**: `dd_logic/lbo_dd/calculations/`
  - `lbo_model.md`: LBOモデル構築の数式仕様書
  - `dcf_analysis.md`: DCF分析の数式仕様書
- **ワークフロー**: `agents/workflows/lbo_dd_workflow.md`
- **レポートテンプレート**: `dd_logic/lbo_dd/outputs/report_template.md`
