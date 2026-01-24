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
    ├── common/              # 共通モジュール
    │   └── pdf_parser.py   # PDF解析共通機能
    ├── nn_dd/               # NN DDロジック
    │   ├── criteria/        # 評価基準
    │   ├── calculations/    # 計算ロジック
    │   ├── extractors/      # PDF数値抽出モジュール
    │   ├── workflows/       # ワークフロー
    │   └── outputs/         # 出力フォーマット
    ├── im_dd/               # IM DDロジック
    │   ├── evaluation_points/  # 評価論点
    │   ├── calculations/    # 計算ロジック
    │   ├── extractors/      # 財務諸表抽出モジュール
    │   ├── workflows/       # ワークフロー
    │   └── outputs/         # 出力フォーマット
    ├── workflows/           # 統合ワークフロー
    │   └── deal_processor.py # 案件処理モジュール
    ├── additional_dd/       # 追加DD用フォーマット
    │   └── templates/       # 議論用テンプレート
    ├── references/          # PEファンドDDロジック文献
    └── evaluation_points_manager.py  # 論点管理システム
```

## 🔄 ワークフロー

### 1. NN DDフロー（Non Name Sheet）
- **入力**: NN資料（PDF/MDファイル）
- **処理**: 定量・定性情報を基にした自動評価
  - PDF/MDファイルの自動読み込み
  - PDFから表を抽出して基本的な財務数値を抽出（簡易版）
  - 評価基準に基づく評価
  - 既存の計算ロジックの適用（`nn_dd_calculator.py`）
  - 定量・定性情報を統合した結論の導出
- **出力**: NN DD結果レポート（`dd_results/nn_dd/report.md` + `data.json`）

### 2. IM DDフロー（Information Memorandum）
- **入力**: IM資料（PDF）
- **処理**: 定量・定性情報を基にした評価
  - PDFから財務諸表（BS、PL、CF）を詳細に抽出
  - 財務諸表データを基に分析
  - 既存のDCF分析ロジックの適用
  - 評価論点に基づく評価
  - 定量・定性情報を統合した結論の導出
- **出力**: IM DD結果レポート（`dd_results/im_dd/report.md` + `data.json`）

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

### 自動ワークフロー実行（推奨）

#### 案件の自動処理（NN DD + IM DD）
```python
from dd_logic.workflows.deal_processor import process_deal

# 案件ディレクトリを指定して自動処理
result = process_deal("deals/[deal_name]")
```

#### NN DDのみ実行
```python
result = process_deal("deals/[deal_name]", process_type="nn")
```

#### IM DDのみ実行
```python
result = process_deal("deals/[deal_name]", process_type="im")
```

### 手動実行

#### NN DDの実行
1. NN資料（PDF/MD）を `deals/[deal_name]/nn/` に配置
2. 以下のコマンドで実行:
   ```python
   from dd_logic.nn_dd.workflows.nn_dd_workflow import run_nn_dd_workflow
   result = run_nn_dd_workflow("deals/[deal_name]")
   ```
3. 結果が `deals/[deal_name]/dd_results/nn_dd/` に自動保存されます

#### IM DDの実行
1. IM資料（PDF）を `deals/[deal_name]/im/` に配置
2. 以下のコマンドで実行:
   ```python
   from dd_logic.im_dd.workflows.im_dd_workflow import run_im_dd_workflow
   result = run_im_dd_workflow("deals/[deal_name]")
   ```
3. 結果が `deals/[deal_name]/dd_results/im_dd/` に自動保存されます

### Agentsコマンド（Cursor内で使用）
- `/deal:process [deal_name]` - 案件の自動処理（NN DD + IM DD）
- `/deal:process_nn [deal_name]` - NN DDのみ実行
- `/deal:process_im [deal_name]` - IM DDのみ実行

### PDF解析機能

#### NN DD用簡易PDF数値抽出
```python
from dd_logic.nn_dd.extractors.simple_financial_extractor import extract_simple_financials

# PDFから基本的な財務数値を抽出（EBITDA、Net Debt等）
financial_data = extract_simple_financials("path/to/file.pdf")
```

#### IM DD用詳細財務諸表抽出
```python
from dd_logic.im_dd.extractors.financial_statement_extractor import extract_financial_statements

# PDFから財務諸表（BS、PL、CF）を詳細に抽出
statements = extract_financial_statements("path/to/file.pdf")
```

### 計算ロジックの使用
- NN DD計算: `dd_logic/nn_dd/calculations/nn_dd_calculator.py`
- 財務指標計算: `dd_logic/nn_dd/calculations/financial_metrics.py`
- バリュエーション指標計算: `dd_logic/nn_dd/calculations/valuation_metrics.py`
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

## 📦 インストール

```bash
pip install -r requirements.txt
```

必要な依存関係:
- `pdfplumber`: PDF解析と表抽出
- `pandas`: 財務諸表データの処理

## ⚠️ 注意事項

- 案件データは機密情報を含むため、`.gitignore`で除外されています
- 計算ロジックは参考実装であり、実際の投資判断には適切な検証が必要です
- 各案件の評価は、必ず人間による最終判断を経てください
- PDF解析は簡易版のため、複雑な形式のPDFでは正確に抽出できない場合があります
- 定性情報の抽出には、AI/LLMを使用することを推奨します（現在は簡易実装）
