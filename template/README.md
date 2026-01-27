# 案件テンプレート

## 概要
新規案件を作成する際のテンプレートです。このテンプレートをコピーして、各投資案件のディレクトリを作成します。

## ディレクトリ構造
```
[deal_name]/
├── nn/              # Non Name Sheet関連資料（入力）
│   ├── materials/   # 元資料（PDF/Web/md）
│   └── processed/  # 処理済みデータ（構造化されたデータ）
├── im/              # Information Memorandum関連資料（入力）
│   ├── materials/   # 元資料（PDF）
│   └── processed/  # 処理済みデータ（構造化されたデータ）
├── vdr/             # VDR（Virtual Data Room）関連資料
│   ├── nn/         # NN関連VDR資料
│   ├── im/         # IM関連VDR資料
│   └── memo/       # メモ・補足資料
├── dd_results/     # DD結果（集約管理）
│   ├── nn_dd/      # NN DD結果
│   ├── im_dd/      # IM DD結果
│   ├── lbo_dd/     # LBO DD結果
│   └── additional_dd/ # 追加DD結果
├── ai_dd_results/  # AIによるDD結果（自動生成）
│   ├── nn_dd/      # AIによるNN DD結果
│   ├── im_dd/      # AIによるIM DD結果
│   └── lbo_dd/     # AIによるLBO DD結果
├── human_dd_note/  # 人間によるDDノート
└── others/         # その他資料
```

## 使用方法

### 新規案件の作成
1. このテンプレートディレクトリ（`deals/template/`）をコピー
2. 案件名をディレクトリ名に設定（例: `deals/[deal_name]/`）
3. 各ディレクトリに資料を配置

### ワークフローの実行
- **NN DD**: NN資料を `nn/materials/` に配置後、NN DDワークフローを実行
  - 詳細: `agents/workflows/nn_dd_workflow.md` を参照
  - 結果: `dd_results/nn_dd/` または `ai_dd_results/nn_dd/` に保存
- **IM DD**: IM資料を `im/materials/` に配置後、IM DDワークフローを実行
  - 詳細: `agents/workflows/im_dd_workflow.md` を参照
  - 結果: `dd_results/im_dd/` または `ai_dd_results/im_dd/` に保存
- **LBO DD**: LBOモデルを構築し、実行判断の意思決定を行う
  - 詳細: `agents/workflows/lbo_dd_workflow.md` を参照（今後追加予定）
  - 結果: `dd_results/lbo_dd/` または `ai_dd_results/lbo_dd/` に保存
- **追加DD**: 人間による議論・追加調査の結果を `dd_results/additional_dd/` に保存

### 実装方法
全ての計算ロジックはmd形式の数式仕様書として記述されています。AI/LLMを使用したプロンプトベースで実装可能です。

## 各ディレクトリの詳細
- `nn/`: Non Name Sheet関連資料の管理
- `im/`: Information Memorandum関連資料の管理
- `vdr/`: VDR（Virtual Data Room）関連資料の管理
- `dd_results/`: DD結果の集約管理（人間による最終判断を含む）
- `ai_dd_results/`: AIによるDD結果（自動生成）
- `human_dd_note/`: 人間によるDDノート
- `others/`: その他資料の管理

## 関連ドキュメント
- プロジェクト全体の説明: `/README.md`
- 案件管理ディレクトリ: `/deals/README.md`
