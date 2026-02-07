# 案件テンプレート

## 概要
新規案件を作成する際のテンプレートです。このテンプレートをコピーして、各投資案件のディレクトリを作成します。

## ディレクトリ構造
```
[deal_name]/
├── vdr/             # VDR（Virtual Data Room）関連資料
│   ├── nn/         # NN関連VDR資料
│   ├── im/         # IM関連VDR資料
│   └── memo/       # メモ・補足資料
├── ai_dd_results/  # AIによるDD結果（自動生成）
│   ├── nn_dd/      # AIによるNN DD結果
│   ├── im_dd/      # AIによるIM DD結果
│   └── lbo_dd/     # AIによるLBO DD結果
└── human_dd_note/  # 人間によるDDノート
```

## 使用方法

### 新規案件の作成
1. このテンプレートディレクトリ（`dd_logic/template_deal/`）をコピー
2. コピー先を `deals/[deal_name]/` とする（案件名をディレクトリ名に設定）
3. 各ディレクトリに資料を配置

### ワークフローの実行
- **NN DD**: VDR資料を `vdr/nn/` に配置後、NN DDワークフローを実行
  - 詳細: `.cursor/skills/pe-dd-nn/workflow.md` を参照
  - 結果: `ai_dd_results/nn_dd/` に保存
- **IM DD**: VDR資料を `vdr/im/` に配置後、IM DDワークフローを実行
  - 詳細: `.cursor/skills/pe-dd-im/workflow.md` を参照
  - 結果: `ai_dd_results/im_dd/` に保存
- **LBO DD**: VDR資料を `vdr/im/` に配置後、LBO DDワークフローを実行
  - 詳細: `.cursor/skills/pe-dd-lbo/workflow.md` を参照
  - 結果: `ai_dd_results/lbo_dd/` に保存
- **追加DD**: 人間による議論・追加調査の結果を `human_dd_note/` に保存

### 実装方法
全ての計算ロジックはmd形式の数式仕様書として記述されています。AI/LLMを使用したプロンプトベースで実装可能です。

## 各ディレクトリの詳細
- `vdr/`: VDR（Virtual Data Room）関連資料の管理
  - `nn/`: NN関連VDR資料
  - `im/`: IM関連VDR資料
  - `memo/`: メモ・補足資料
- `ai_dd_results/`: AIによるDD結果（自動生成）
  - `nn_dd/`: AIによるNN DD結果
  - `im_dd/`: AIによるIM DD結果
  - `lbo_dd/`: AIによるLBO DD結果
- `human_dd_note/`: 人間によるDDノート

## 関連ドキュメント
- プロジェクト全体の説明: `/README.md`
- 案件管理ディレクトリ: `/deals/README.md`
