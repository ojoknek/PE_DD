# PE_DD - PEファンド向けデューデリジェンスワークフロー

PEファンド向けのデューデリジェンス（DD）ワークフローをCursorで実装・管理するためのリポジトリです。

## 📁 ディレクトリ構成

```
PE_DD/
├── deals/                    # 案件管理ディレクトリ
│   └── [deal_name]/         # 案件単位のディレクトリ（動的に追加）
│       ├── vdr/            # VDR（Virtual Data Room）関連資料
│       │   ├── nn/         # NN関連VDR資料
│       │   ├── im/         # IM関連VDR資料
│       │   └── memo/       # メモ・補足資料
│       ├── ai_dd_results/  # AIによるDD結果（自動生成）
│       │   ├── nn_dd/      # AIによるNN DD結果
│       │   ├── im_dd/      # AIによるIM DD結果
│       │   └── lbo_dd/     # AIによるLBO DD結果
│       └── human_dd_note/  # 人間によるDDノート
│
├── .cursor/skills/           # Cursorスキル（ワークフロー・プロンプト・コマンド）
│   ├── pe-dd-nn/            # NN DDスキル（prompts/, workflow.md）
│   ├── pe-dd-im/            # IM DDスキル（prompts/, workflow.md）
│   ├── pe-dd-lbo/           # LBO DDスキル（prompts/, workflow.md）
│   └── pe-dd-deal/          # 案件管理・DD一括実行（commands.md）
│
└── dd_logic/                # DDプロセスロジック
    ├── template_deal/       # 案件テンプレート（新規案件作成時にコピー元）
    ├── nn_dd/               # NN DDロジック
    │   ├── criteria/        # 評価基準
    │   │   └── evaluation_criteria.md
    │   ├── calculations/    # 計算ロジック（数式仕様書）
    │   │   ├── nn_dd_calculator.md
    │   │   ├── financial_metrics.md
    │   │   ├── valuation_metrics.md
    │   │   └── README.md
    │   ├── evaluation_points/  # 評価論点
    │   │   └── evaluation_points.md
    │   └── outputs/         # 出力フォーマット
    │       └── report_template.md
    ├── im_dd/               # IM DDロジック
    │   ├── evaluation_points/  # 評価論点
    │   │   └── evaluation_points.md
    │   ├── calculations/    # 計算ロジック（数式仕様書）
    │   │   ├── dcf_analysis.md
    │   │   └── README.md
    │   └── outputs/         # 出力フォーマット
    │       └── report_template.md
    ├── lbo_dd/              # LBO DDロジック
    │   ├── evaluation_points/  # 評価論点
    │   │   └── evaluation_points.md
    │   ├── calculations/    # 計算ロジック（数式仕様書）
    │   │   ├── dcf_analysis.md
    │   │   └── README.md
    │   └── outputs/         # 出力フォーマット
    │       └── report_template.md
    ├── additional_dd/       # 追加DD用フォーマット
    │   └── templates/       # 議論用テンプレート
    ├── references/          # PEファンドDDロジック文献
    ├── evaluation_points.md # 評価論点フレームワーク（仕様書）
    └── README.md            # DDロジック全体の説明
```

## 🔄 ワークフロー

### 1. NN DDフロー（Non Name Sheet）
- **入力**: VDR資料（`deals/[deal_name]/vdr/nn/` 配下のPDF/MDファイル）
- **処理**: 定量・定性情報を基にした評価
  - 評価基準に基づく評価（`dd_logic/nn_dd/criteria/evaluation_criteria.md`）
  - 計算ロジックの適用（数式仕様書を参照）
    - 中間計算（ND/EBITDA、EV、Equity Value、定性合計）
    - 定量判定（離散判定：◎/〇/△/×）
    - ゲート判定（定量ゲート、定性ゲート）
    - 最終判定（見送り/見送りでない）
  - 定量・定性情報を統合した結論の導出
- **出力**: NN DD結果レポート（`deals/[deal_name]/ai_dd_results/nn_dd/report.md`）

### 2. IM DDフロー（Information Memorandum）
- **入力**: VDR資料（`deals/[deal_name]/vdr/im/` 配下のPDFファイル）
- **処理**: 定量・定性情報を基にした評価
  - 評価論点に基づく評価（`dd_logic/im_dd/evaluation_points/evaluation_points.md`）
  - DCF分析ロジックの適用（数式仕様書を参照）
    - FCF計算
    - WACC計算
    - ターミナル・バリュー計算
    - 企業価値（EV）計算
  - 定量・定性情報を統合した結論の導出
- **出力**: IM DD結果レポート（`deals/[deal_name]/ai_dd_results/im_dd/report.md`）

### 3. LBO DDフロー（Leveraged Buyout）
- **入力**: VDR資料（`deals/[deal_name]/vdr/im/` 配下のPDFファイル）、財務モデル
- **処理**: LBOモデルを構築し、実行判断の意思決定を行う
  - 評価論点に基づく評価（`dd_logic/lbo_dd/evaluation_points/evaluation_points.md`）
  - LBOモデルの構築
    - レバレッジ比率の設定
    - 負債スケジュールの構築
    - エクイティ・コントリビューションの計算
  - 実行判断の評価
    - IRR（内部収益率）の計算
    - MOIC（Multiple of Invested Capital）の計算
    - キャッシュスイープモデルの構築
  - 定量・定性情報を統合した結論の導出
- **出力**: LBO DD結果レポート（`deals/[deal_name]/ai_dd_results/lbo_dd/report.md`）

### 4. 追加DDフロー
- **入力**: 人間による議論・追加調査
- **処理**: フォーマットに沿った記録・分析
  - 議論テーマの設定
  - 調査・議論の実施
  - 結果の整理
- **出力**: 追加DD結果（`deals/[deal_name]/human_dd_note/` に保存）

## 🚀 使い方

### 新規案件の作成
1. `dd_logic/template_deal/` をコピーして新規案件ディレクトリを作成（`deals/[deal_name]/`）
2. 案件名をディレクトリ名に設定
3. 各ディレクトリに資料を配置

### 計算ロジックの参照

全ての計算ロジックはmd形式の数式仕様書として記述されています。AI/LLMを使用したプロンプトベースで実装可能です。

#### NN DD計算ロジック
- **メイン計算**: `dd_logic/nn_dd/calculations/nn_dd_calculator.md`
  - 中間計算（ND/EBITDA、EV、Equity Value、定性合計）
  - 定量判定（離散判定：◎/〇/△/×）
  - ゲート判定（定量ゲート、定性ゲート）
  - 最終判定（見送り/見送りでない）
- **財務指標計算**: `dd_logic/nn_dd/calculations/financial_metrics.md`
  - CAGR、EBITDAマージン、ROE、ROA等
  - 流動比率、当座比率、運転資金等
- **バリュエーション指標**: `dd_logic/nn_dd/calculations/valuation_metrics.md`
  - Net Debt、EV、Equity Valueの計算

#### IM DD計算ロジック
- **DCF分析**: `dd_logic/im_dd/calculations/dcf_analysis.md`
  - FCF計算プロセス
  - WACC計算（CAPM、ベータのアンレバリング/リレバリング）
  - ターミナル・バリュー計算（Gordon Growth Model）
  - 企業価値（EV）計算

#### LBO DD計算ロジック
- **DCF分析**: `dd_logic/lbo_dd/calculations/dcf_analysis.md`
  - FCF計算プロセス
  - WACC計算
  - ターミナル・バリュー計算
  - 企業価値（EV）計算
- **LBOモデル構築**（今後追加予定）
  - レバレッジ比率の設定
  - 負債スケジュールの構築
  - エクイティ・コントリビューションの計算
  - IRR・MOICの計算
  - キャッシュスイープモデルの構築

#### 評価論点フレームワーク
- **評価論点**: `dd_logic/evaluation_points.md`
  - NN DD/IM DD/LBO DDの評価論点定義
  - 定量論点・定性論点の構造
  - スコア計算式

## 📚 主要ファイル

### ワークフロー・プロンプト（Cursor Skills）
- `.cursor/skills/pe-dd-nn/workflow.md`: NN DDワークフロー（プロンプト: `prompts/`）
- `.cursor/skills/pe-dd-im/workflow.md`: IM DDワークフロー（プロンプト: `prompts/`）
- `.cursor/skills/pe-dd-lbo/workflow.md`: LBO DDワークフロー（プロンプト: `prompts/`）
- `.cursor/skills/pe-dd-deal/commands.md`: 擬似コマンド一覧
- 詳細: `.cursor/skills/README.md`

### 評価基準・論点
- `dd_logic/nn_dd/criteria/evaluation_criteria.md`: NN DD評価基準
- `dd_logic/im_dd/evaluation_points/evaluation_points.md`: IM DD評価論点
- `dd_logic/lbo_dd/evaluation_points/evaluation_points.md`: LBO DD評価論点

### 計算ロジック（数式仕様書）
- `dd_logic/nn_dd/calculations/`: NN DD計算ロジック（md形式の数式仕様書）
  - `nn_dd_calculator.md`: NN DD計算ロジックの数式仕様書
  - `financial_metrics.md`: 財務指標計算の数式仕様書
  - `valuation_metrics.md`: バリュエーション指標計算の数式仕様書
  - `README.md`: NN DD計算ロジックの概要
- `dd_logic/im_dd/calculations/`: IM DD計算ロジック（md形式の数式仕様書）
  - `dcf_analysis.md`: DCF分析の数式仕様書
  - `README.md`: IM DD計算ロジックの概要
- `dd_logic/lbo_dd/calculations/`: LBO DD計算ロジック（md形式の数式仕様書）
  - `dcf_analysis.md`: DCF分析の数式仕様書
  - `README.md`: LBO DD計算ロジックの概要
- `dd_logic/evaluation_points.md`: 評価論点フレームワークの仕様書

### プロンプト
- `.cursor/skills/pe-dd-nn/prompts/`: NN DD用プロンプト
- `.cursor/skills/pe-dd-im/prompts/`: IM DD用プロンプト
- `.cursor/skills/pe-dd-lbo/prompts/`: LBO DD用プロンプト

### 参考文献
- `dd_logic/references/`: PEファンドDDロジックに関する文献

## 🔧 カスタマイズ

### 評価論点のカスタマイズ
`dd_logic/evaluation_points.md` を参照して評価論点を管理・カスタマイズできます。

### 計算ロジックの参照
各計算ロジックはmd形式の数式仕様書として記述されています。数式を参照して、AI/LLMを使用したプロンプトベースで実装可能です。

## 📚 参考リポジトリ

本リポジトリは [DD_template](https://github.com/ojoknek/DD_template) を参考に作成されています。

## 📦 インストール

本リポジトリは計算ロジックをmd形式の数式仕様書として提供しているため、特別な依存関係は不要です。AI/LLMを使用したプロンプトベースで実装可能です。

## ⚠️ 注意事項

- 案件データは機密情報を含むため、`.gitignore`で除外されています
- 計算ロジックは数式仕様書として記述されており、実際の投資判断には適切な検証が必要です
- 各案件の評価は、必ず人間による最終判断を経てください
- 数式仕様書を参照して、AI/LLMを使用したプロンプトベースで実装してください
- 定性情報の評価には、AI/LLMを使用することを推奨します

---

作成者: ojoknek 
用途: PEファンドによるM&A検討企業への投資判断・デューデリジェンス 
ライセンス: 本ドキュメントの著作権は ojoknek に帰属し、無断転載・配布を禁じます。
