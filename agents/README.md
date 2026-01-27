# エージェント関連ディレクトリ

## 概要
エージェント関連のプログラムや案件DD・ロジックを指南するプロンプト関連をまとめたディレクトリです。AI/LLMを使用したプロンプトベースでDDプロセスを実行するためのリソースを提供します。

## ディレクトリ構成

### prompts/
メタプロンプト集
- `nn_dd/`: NN DD用プロンプト
  - `load_materials_prompt.md`: 資料読み込みプロンプト
  - `evaluate_prompt.md`: NN DD評価プロンプト
  - `README.md`: NN DD用プロンプトの説明
- `im_dd/`: IM DD用プロンプト
  - `load_im_prompt.md`: IM読み込みプロンプト
  - `evaluate_prompt.md`: IM DD評価プロンプト
  - `README.md`: IM DD用プロンプトの説明
- `lbo_dd/`: LBO DD用プロンプト（今後追加予定）

### workflows/
ワークフロー定義
- `nn_dd_workflow.md`: NN DDワークフロー
- `im_dd_workflow.md`: IM DDワークフロー
- `lbo_dd_workflow.md`: LBO DDワークフロー（今後追加予定）
- `additional_dd_workflow.md`: 追加DDワークフロー

### commands/
擬似コマンド定義
- `README.md`: コマンド一覧と使用方法
- Cursorで使用する擬似スラッシュコマンドの定義

## 使用方法
各ワークフローに従って、対応するプロンプトを使用します。計算ロジックは数式仕様書（`dd_logic/`配下）を参照して、適切な計算式を適用してください。
