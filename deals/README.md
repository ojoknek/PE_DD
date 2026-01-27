# 案件管理ディレクトリ

## 概要
各投資案件を管理するディレクトリです。各案件は独立したディレクトリとして管理され、NN DD、IM DD、LBO DDの結果を集約管理します。

## 構造
```
deals/
└── [deal_name]/    # 案件単位のディレクトリ（動的に追加）
    ├── vdr/            # VDR（Virtual Data Room）関連資料
    │   ├── nn/         # NN関連VDR資料
    │   ├── im/         # IM関連VDR資料
    │   └── memo/       # メモ・補足資料
    ├── ai_dd_results/  # AIによるDD結果（自動生成）
    │   ├── nn_dd/      # AIによるNN DD結果
    │   ├── im_dd/      # AIによるIM DD結果
    │   └── lbo_dd/     # AIによるLBO DD結果
    └── human_dd_note/  # 人間によるDDノート
```

## 新規案件の作成
1. `agents/template_deal/` をコピーして新規案件ディレクトリを作成（`deals/[deal_name]/`）
2. 案件名をディレクトリ名に設定
3. 各ディレクトリに資料を配置

## DDプロセスの実行
- **NN DD**: VDR資料を `vdr/nn/` に配置後、NN DDワークフローを実行
  - 結果: `ai_dd_results/nn_dd/` に保存
- **IM DD**: VDR資料を `vdr/im/` に配置後、IM DDワークフローを実行
  - 結果: `ai_dd_results/im_dd/` に保存
- **LBO DD**: VDR資料を `vdr/im/` に配置後、LBO DDワークフローを実行
  - 結果: `ai_dd_results/lbo_dd/` に保存
- **追加DD**: 人間による議論・追加調査の結果を `human_dd_note/` に保存

## 案件一覧
各案件は独立したディレクトリとして管理されます。
