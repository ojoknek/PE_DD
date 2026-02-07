# LBO DD結果

## 概要
LBO（Leveraged Buyout）モデルを基にしたLBO DD評価の結果を管理するディレクトリです。LBO DDワークフロー実行時に自動生成され、このディレクトリに保存されます。

## ファイル構成
- `report.md`: AIによるLBO DD結果レポート（人間が読みやすい形式）
  - 評価結果のサマリー
  - LBOモデルの構築結果
  - 実行判断の評価
  - IRR・MOIC等の計算結果
  - 総合スコアと投資推奨度

## 評価内容
LBO DDでは以下の評価が実施されます：
- **LBOモデルの構築**:
  - レバレッジ比率の設定
  - 負債スケジュールの構築
  - エクイティ・コントリビューションの計算
- **実行判断の評価**:
  - IRR（内部収益率）の計算
  - MOIC（Multiple of Invested Capital）の計算
  - キャッシュスイープモデルの構築
  - リスク分析
- **スコア算出**:
  - 総合スコア
  - 投資推奨度の算出

## 使用方法

### 1. 入力資料の配置
VDR資料を `../../vdr/im/` に配置します（必須）。
- IM関連VDR資料（PDF等）
- 財務諸表データ
- 事業計画データ

### 2. ワークフローの実行
LBO DDワークフローを実行します。
- 詳細な手順: `.cursor/skills/pe-dd-lbo/workflow.md` を参照
- AI/LLMを使用したプロンプトベースで実装
- 計算ロジックは数式仕様書（`dd_logic/lbo_dd/calculations/`）を参照
  - `dcf_analysis.md`: DCF分析の数式仕様書
  - `lbo_model.md`: LBOモデル構築の数式仕様書

### 3. 結果の確認
結果がこのディレクトリに自動的に生成されます：
- `report.md`: LBO DD結果レポート（実行判断を含む）を確認

## 評価内容の詳細

### LBOモデルの構築
- レバレッジ比率の設定
- 負債スケジュールの構築（キャッシュスイープ付き）
- エクイティ・コントリビューションの計算
- 財務3表の構築（18ステップ）

### リターン分析
- IRR（内部収益率）の計算
- MOIC（Multiple of Invested Capital）の計算
- 売却時のEVと株式価値の計算
- 年別IRRシミュレーション

### 安全性分析
- レバレッジレシオ（Leverage Ratio）
- インタレストカバレッジレシオ（Interest Coverage Ratio）
- デットサービスカバレッジレシオ（DSCR）
- コベナンツ（財務制限条項）のチェック

### 感応度分析
- 買収プレミアムの変化による影響
- 売却倍率の変化による影響
- 売却年度の変化による影響

## 評価論点
詳細な評価論点は以下を参照してください：
- `dd_logic/lbo_dd/evaluation_points/evaluation_points.md`: LBO DD評価論点

## 関連ディレクトリ
- **入力資料**: `../../vdr/im/` - IM関連VDR資料（必須）
- **評価ロジック**: `dd_logic/lbo_dd/` - LBO DD評価ロジック
- **ワークフロー定義**: `.cursor/skills/pe-dd-lbo/workflow.md` - LBO DDワークフロー
