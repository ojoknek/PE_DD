# 案件テンプレート

## 概要
新規案件を作成する際のテンプレートです。

## ディレクトリ構造
```
[deal_name]/
├── nn/              # Non Name Sheet関連資料
│   ├── materials/   # 元資料（PDF/Web/md）
│   └── processed/  # 処理済みデータ
├── im/              # Information Memorandum関連資料
│   ├── materials/   # 元資料（PDF）
│   └── processed/  # 処理済みデータ
├── dd_results/     # DD結果（集約管理）
│   ├── nn_dd/      # NN DD結果
│   ├── im_dd/      # IM DD結果
│   └── additional_dd/ # 追加DD結果
└── others/         # その他資料
```

## 使用方法
1. このテンプレートをコピーして新規案件ディレクトリを作成
2. 案件名をディレクトリ名に設定
3. 各ディレクトリに資料を配置
