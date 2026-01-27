# 案件管理ディレクトリ

## 概要
各投資案件を管理するディレクトリです。各案件は独立したディレクトリとして管理され、NN DD、IM DD、LBO DDの結果を集約管理します。

## 構造
```
deals/
├── template/        # 案件テンプレート
└── [deal_name]/    # 案件単位のディレクトリ（動的に追加）
    ├── nn/              # Non Name Sheet関連資料（入力）
    ├── im/              # Information Memorandum関連資料（入力）
    ├── dd_results/     # DD結果（集約管理）
    │   ├── nn_dd/      # NN DD結果
    │   ├── im_dd/      # IM DD結果
    │   ├── lbo_dd/     # LBO DD結果
    │   └── additional_dd/ # 追加DD結果
    └── others/         # その他資料
```

## 新規案件の作成
1. `template/` をコピーして新規案件ディレクトリを作成
2. 案件名をディレクトリ名に設定
3. 各ディレクトリに資料を配置

## DDプロセスの実行
- **NN DD**: NN資料を `nn/` に配置後、NN DDワークフローを実行
- **IM DD**: IM資料を `im/` に配置後、IM DDワークフローを実行
- **LBO DD**: LBOモデルを構築し、実行判断の意思決定を行う
- **追加DD**: 人間による議論・追加調査の結果を `dd_results/additional_dd/` に保存

## 案件一覧
各案件は独立したディレクトリとして管理されます。
