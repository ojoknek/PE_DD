# PE_DD - PEファンド向けデューデリジェンスワークフロー

PEファンド向けのデューデリジェンス（DD）ワークフローをCursorで実装・管理するためのリポジトリです。

## 📁 ディレクトリ構成

```
PE_DD/
├── deals/                    # 案件管理ディレクトリ
│   ├── template/            # 案件テンプレート
│   └── [deal_name]/         # 案件単位のディレクトリ（動的に追加）
│       ├── nn/              # Non Name Sheet関連資料（入力）
│       ├── im/              # Information Memorandum関連資料（入力）
│       ├── dd_results/      # DD結果（集約管理）
│       │   ├── nn_dd/      # NN DD結果
│       │   ├── im_dd/      # IM DD結果
│       │   └── additional_dd/ # 追加DD結果
│       └── others/         # その他資料
│
├── agents/                   # エージェント関連ディレクトリ
│   ├── prompts/             # メタプロンプト集
│   │   ├── nn_dd/          # NN DD用プロンプト
│   │   ├── im_dd/          # IM DD用プロンプト
│   │   └── additional_dd/  # 追加DD用プロンプト
│   ├── workflows/           # ワークフロー定義
│   │   ├── nn_dd_workflow.md
│   │   ├── im_dd_workflow.md
│   │   └── additional_dd_workflow.md
│   └── commands/            # 擬似コマンド定義
│
└── dd_logic/                # DDプロセスロジック
    ├── nn_dd/               # NN DDロジック
    │   ├── criteria/        # 評価基準
    │   ├── calculations/    # 計算ロジック
    │   └── outputs/         # 出力フォーマット
    ├── im_dd/               # IM DDロジック
    │   ├── evaluation_points/  # 評価論点
    │   ├── calculations/    # 計算ロジック
    │   └── outputs/         # 出力フォーマット
    ├── additional_dd/       # 追加DD用フォーマット
    │   └── templates/       # 議論用テンプレート
    ├── references/          # PEファンドDDロジック文献
    └── evaluation_points_manager.py  # 論点管理システム
```

## 🔄 ワークフロー

### 1. NN DDフロー（Non Name Sheet）
- **入力**: NN資料（PDF/Web/mdファイル）
- **処理**: 定量・定性情報を基にした自動評価
  - 資料の読み込みと構造化
  - 評価基準に基づく評価
  - 計算ロジックの適用（財務指標、バリュエーション指標、スコアリング）
  - 定量・定性情報を統合した結論の導出
- **出力**: NN DD結果レポート（Markdown + JSON）

### 2. IM DDフロー（Information Memorandum）
- **入力**: IM資料（PDF）
- **処理**: 定量・定性情報を基にした評価
  - IMの読み込みと解析
  - 評価論点に基づく評価
  - 計算ロジックの適用（DCF分析、バリュエーション分析、リスク分析）
  - 定量・定性情報を統合した結論の導出
- **出力**: IM DD結果レポート（Markdown + JSON）

### 3. 追加DDフロー
- **入力**: 人間による議論・追加調査
- **処理**: フォーマットに沿った記録・分析
  - 議論テーマの設定
  - 調査・議論の実施
  - 結果の整理
- **出力**: 追加DD結果（テンプレートに基づく）

## 🚀 使い方

### 新規案件の作成
1. `deals/template/` をコピーして新規案件ディレクトリを作成
2. 案件名をディレクトリ名に設定
3. 各ディレクトリに資料を配置

### NN DDの実行
1. NN資料を `deals/[deal_name]/nn/materials/` に配置
2. NN DDワークフローを実行（`agents/workflows/nn_dd_workflow.md`を参照）
3. 結果が `deals/[deal_name]/dd_results/nn_dd/` に保存されます

### IM DDの実行
1. IM資料を `deals/[deal_name]/im/materials/` に配置
2. IM DDワークフローを実行（`agents/workflows/im_dd_workflow.md`を参照）
3. 結果が `deals/[deal_name]/dd_results/im_dd/` に保存されます

### 計算ロジックの使用
- 財務指標計算: `dd_logic/nn_dd/calculations/financial_metrics.py`
- バリュエーション指標計算: `dd_logic/nn_dd/calculations/valuation_metrics.py`
- スコアリング: `dd_logic/nn_dd/calculations/scoring.py`
- DCF分析: `dd_logic/im_dd/calculations/dcf_analysis.py`
- 論点管理: `dd_logic/evaluation_points_manager.py`

## 📚 主要ファイル

### ワークフロー定義
- `agents/workflows/nn_dd_workflow.md`: NN DDワークフロー
- `agents/workflows/im_dd_workflow.md`: IM DDワークフロー
- `agents/workflows/additional_dd_workflow.md`: 追加DDワークフロー

### 評価基準・論点
- `dd_logic/nn_dd/criteria/evaluation_criteria.md`: NN DD評価基準
- `dd_logic/im_dd/evaluation_points/evaluation_points.md`: IM DD評価論点

### 計算ロジック
- `dd_logic/nn_dd/calculations/`: NN DD計算ロジック
- `dd_logic/im_dd/calculations/`: IM DD計算ロジック

### プロンプト
- `agents/prompts/nn_dd/`: NN DD用プロンプト
- `agents/prompts/im_dd/`: IM DD用プロンプト
- `agents/prompts/additional_dd/`: 追加DD用プロンプト

### 参考文献
- `dd_logic/references/`: PEファンドDDロジックに関する文献

## 🔧 カスタマイズ

### 評価論点のカスタマイズ
`dd_logic/evaluation_points_manager.py` を使用して評価論点を管理・カスタマイズできます。

### 計算ロジックの拡張
各計算ロジックはPythonスクリプトとして実装されているため、必要に応じて拡張可能です。

## 📚 参考リポジトリ

本リポジトリは [DD_template](https://github.com/ojoknek/DD_template) を参考に作成されています。

## ⚠️ 注意事項

- 案件データは機密情報を含むため、`.gitignore`で除外されています
- 計算ロジックは参考実装であり、実際の投資判断には適切な検証が必要です
- 各案件の評価は、必ず人間による最終判断を経てください
