# 擬似コマンド定義

## 概要
Cursorで使用する擬似スラッシュコマンドの定義です。各スキル（pe-dd-nn / pe-dd-im / pe-dd-lbo / pe-dd-deal）が対応するアクションを実行します。

## コマンド一覧

### NN DD関連
- `/nn_dd:init` - NN DDの初期化
- `/nn_dd:load` - 資料の読み込み
- `/nn_dd:evaluate` - NN DD評価の実行
- `/nn_dd:report` - 結果レポートの生成

### IM DD関連
- `/im_dd:init` - IM DDの初期化
- `/im_dd:load_im` - IMの読み込み
- `/im_dd:evaluate` - IM DD評価の実行
- `/im_dd:report` - 結果レポートの生成

### LBO DD関連
- `/lbo_dd:init` - LBO DDの初期化
- `/lbo_dd:build_model` - LBOモデルの構築
- `/lbo_dd:calculate` - LBO計算の実行
- `/lbo_dd:evaluate` - 実行判断の評価
- `/lbo_dd:report` - 結果レポートの生成

### 案件管理関連
- `/deal:create` - 新規案件の作成（詳細: `.cursor/skills/pe-dd-deal-create/`）
- `/deal:list` - 案件一覧の表示
- `/deal:open` - 案件の開く
- `/deal:process [deal_name]` - 案件の自動処理（NN DD + IM DD + LBO DD）
- `/deal:process_nn [deal_name]` - NN DDのみ実行
- `/deal:process_im [deal_name]` - IM DDのみ実行
- `/deal:process_lbo [deal_name]` - LBO DDのみ実行

## 使用方法
Cursorのチャットで `/` に続けてコマンド名を入力します。対応するスキル（`.cursor/skills/pe-dd-*/SKILL.md`）に従ってワークフローが実行されます。
