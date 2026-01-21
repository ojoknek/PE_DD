# Non Name Sheet（NN）関連資料

## 概要
Non Name Sheet（NN）を受け取った段階での入力資料を管理します。

## ディレクトリ構成
- `materials/`: 元資料（PDF/Web/mdファイル）
- `processed/`: 処理済みデータ（構造化されたデータ）

## 使用方法
1. NN資料を `materials/` に配置
2. NN DDワークフローを実行（`agents/workflows/nn_dd_workflow.md`を参照）
3. 処理済みデータが `processed/` に保存されます
4. **DD結果は `../dd_results/nn_dd/` に保存されます**

## 関連ディレクトリ
- DD結果: `../dd_results/nn_dd/`