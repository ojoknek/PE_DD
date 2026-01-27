# DD結果

## 概要
デューデリジェンス（DD）の結果を集約管理するディレクトリです。すべてのDD結果はこのディレクトリ配下に統一して保存されます。

## ディレクトリ構成
- `nn_dd/`: AIによるNN DD結果（Non Name Sheetを基にした評価）
  - 詳細: `nn_dd/README.md` を参照
- `im_dd/`: AIによるIM DD結果（Information Memorandumを基にした評価）
  - 詳細: `im_dd/README.md` を参照
- `lbo_dd/`: AIによるLBO DD結果（LBOモデルを基にした実行判断）
  - 詳細: `lbo_dd/README.md` を参照

## 設計思想
- **AIによる自動生成**: AI/LLMを使用したプロンプトベースでDD結果を自動生成
- **段階的な評価**: NN DD → IM DD → LBO DD という段階的な評価プロセスを反映
- **人間による最終判断**: AI DD結果を踏まえ、人間による追加評価は `human_dd_note/` に記録

## 使用方法

### 自動生成
各DDワークフロー実行後、対応するディレクトリに結果が自動的に生成されます：
- **NN DDワークフロー実行後** → `nn_dd/` に生成
  - `report.md`: NN DD結果レポート
- **IM DDワークフロー実行後** → `im_dd/` に生成
  - `report.md`: IM DD結果レポート
- **LBO DDワークフロー実行後** → `lbo_dd/` に生成
  - `report.md`: LBO DD結果レポート（実行判断を含む）

### 結果の確認
各ディレクトリの `report.md` を確認することで、DD評価結果を把握できます。

## 各ディレクトリの詳細
各ディレクトリの詳細は、それぞれのREADMEを参照してください。
