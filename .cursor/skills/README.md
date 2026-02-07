# Cursor Skills（PE DD）

## 概要
PEファンド向けデューデリジェンス（DD）をCursor上で実行するためのスキル定義です。各スキルはトリガーに応じてワークフロー・プロンプトに従い、DDを実行します。

## スキル一覧

| スキル名 | 説明 | トリガー例 |
|----------|------|------------|
| **pe-dd-nn** | NN DD（Non Name Sheet）の実行 | NN DD、vdr/nn、Non Name |
| **pe-dd-im** | IM DD（Information Memorandum）の実行 | IM DD、vdr/im、IM評価 |
| **pe-dd-lbo** | LBO DD（モデル構築・実行判断）の実行 | LBO DD、LBOモデル、IRR/MOIC |
| **pe-dd-deal** | 案件作成・一覧・DD一括実行 | 新規案件、deal:create、deal:process |

## ディレクトリ構成

各スキルは以下の構成を持ちます（プロンプト・ワークフローはスキル配下に移管済み）。

```
.cursor/skills/
├── README.md           # 本ファイル
├── pe-dd-nn/
│   ├── SKILL.md        # スキル定義（トリガー・ワークフロー概要）
│   ├── workflow.md     # NN DDワークフロー詳細
│   └── prompts/        # NN DD用プロンプト
│       ├── load_materials_prompt.md
│       ├── evaluate_prompt.md
│       └── README.md
├── pe-dd-im/
│   ├── SKILL.md
│   ├── workflow.md
│   └── prompts/
│       ├── load_im_prompt.md
│       ├── evaluate_prompt.md
│       └── README.md
├── pe-dd-lbo/
│   ├── SKILL.md
│   ├── workflow.md
│   └── prompts/
│       ├── load_vdr_prompt.md
│       ├── build_lbo_model_prompt.md
│       ├── evaluate_lbo_prompt.md
│       └── README.md
└── pe-dd-deal/
    ├── SKILL.md        # 案件管理・DD一括実行
    └── commands.md     # 擬似コマンド一覧
```

## 参照関係

- **データ**: `deals/[deal_name]/vdr/`（nn, im, memo）、`deals/[deal_name]/ai_dd_results/`
- **計算ロジック**: `dd_logic/`（nn_dd, im_dd, lbo_dd の evaluation_points, calculations, outputs）
- **テンプレート**: `dd_logic/template_deal/`（新規案件作成時にコピー元）
- **プログラム**: `program/pdf_table_extractor.py`（PDF→PNG変換）

## 使用方法

- Cursor上で「NN DDを実行して」「この案件でLBO DDして」などと依頼すると、対応するスキルに従ってワークフローが実行されます。
- 擬似コマンド（`/deal:create`、`/deal:process` 等）は `.cursor/skills/pe-dd-deal/commands.md` を参照してください。
- 各ワークフローの詳細は各スキル配下の `workflow.md` および `prompts/` を参照してください。
