# DDプロセスロジック

## 概要
PEファンドのデューデリジェンス（DD）プロセスにおける細かいロジックを蓄積するディレクトリです。全ての計算ロジックはmd形式の数式仕様書として記述されており、AI/LLMを使用したプロンプトベースで実装可能です。

## ディレクトリ構成

### template_deal/
案件テンプレート（新規案件作成時にコピー元）
- 本ディレクトリを `deals/[deal_name]/` にコピーして新規案件を作成する
- 詳細: `dd_logic/template_deal/README.md`

### nn_dd/
NN DDロジック（Non Name Sheet用）
- `criteria/`: 評価基準
  - `evaluation_criteria.md`: NN DD評価基準
- `calculations/`: 計算ロジック（数式仕様書）
  - `nn_dd_calculator.md`: NN DD計算ロジックの数式仕様書
  - `financial_metrics.md`: 財務指標計算の数式仕様書
  - `valuation_metrics.md`: バリュエーション指標計算の数式仕様書
  - `README.md`: NN DD計算ロジックの概要
- `evaluation_points/`: 評価論点
  - `evaluation_points.md`: NN DD評価論点
- `outputs/`: 出力フォーマット
  - `report_template.md`: NN DD結果レポートテンプレート

### im_dd/
IM DDロジック（Information Memorandum用）
- `evaluation_points/`: 評価論点
  - `evaluation_points.md`: IM DD評価論点
- `calculations/`: 計算ロジック（数式仕様書）
  - `dcf_analysis.md`: DCF分析の数式仕様書
  - `README.md`: IM DD計算ロジックの概要
- `outputs/`: 出力フォーマット
  - `report_template.md`: IM DD結果レポートテンプレート

### lbo_dd/
LBO DDロジック（Leveraged Buyout用）
- `evaluation_points/`: 評価論点
  - `evaluation_points.md`: LBO DD評価論点
- `calculations/`: 計算ロジック（数式仕様書）
  - `dcf_analysis.md`: DCF分析の数式仕様書
  - `lbo_model.md`: LBOモデル構築の数式仕様書（レバレッジ、負債スケジュール、IRR、MOIC等）
  - `README.md`: LBO DD計算ロジックの概要
- `outputs/`: 出力フォーマット
  - `report_template.md`: LBO DD結果レポートテンプレート（実行判断を含む）

### additional_dd/
追加DD用フォーマット
- `templates/`: 議論・調査用テンプレート

### references/
PEファンドDDロジックに関する文献
- Webから取得したPEファンドのDDロジックに関する文献を蓄積
- 定量・定性情報を統合した結論導出ロジックの参考資料

### evaluation_points.md
評価論点フレームワークの仕様書
- NN DD/IM DD/LBO DDの評価論点を構造化して記述
- 定量論点・定性論点の定義
- ウェイトとクリティカルフラグの定義
- スコア計算式を数式で記述

## 使用方法
各ワークフローで、対応するロジックを参照します。計算ロジックは数式仕様書として記述されているため、AI/LLMを使用したプロンプトベースで実装可能です。
