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
- `lbo_dd/`: LBO DD用プロンプト
  - `load_vdr_prompt.md`: VDR資料読み込みプロンプト
  - `build_lbo_model_prompt.md`: LBOモデル構築プロンプト
  - `evaluate_lbo_prompt.md`: LBO DD評価プロンプト
  - `README.md`: LBO DD用プロンプトの説明

### workflows/
ワークフロー定義
- `nn_dd_workflow.md`: NN DDワークフロー
- `im_dd_workflow.md`: IM DDワークフロー
- `lbo_dd_workflow.md`: LBO DDワークフロー

### template_deal/
案件テンプレート
- 新規案件を作成する際のテンプレートディレクトリ
- `agents/template_deal/` をコピーして `deals/[deal_name]/` を作成
- 詳細: `template_deal/README.md` を参照

### commands/
擬似コマンド定義
- `README.md`: コマンド一覧と使用方法
- Cursorで使用する擬似スラッシュコマンドの定義

## 使用方法
各ワークフローに従って、対応するプロンプトを使用します。計算ロジックは数式仕様書（`dd_logic/`配下）を参照して、適切な計算式を適用してください。
