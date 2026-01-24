# 擬似コマンド定義

## 概要
Cursorで使用する擬似スラッシュコマンドの定義です。

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

### 追加DD関連
- `/additional_dd:init` - 追加DDの初期化
- `/additional_dd:discuss` - 議論テーマの設定
- `/additional_dd:investigate` - 調査の実施
- `/additional_dd:report` - 結果レポートの生成

### 案件管理関連
- `/deal:create` - 新規案件の作成
- `/deal:list` - 案件一覧の表示
- `/deal:open` - 案件の開く
- `/deal:process [deal_name]` - 案件の自動処理（NN DD + IM DD）
- `/deal:process_nn [deal_name]` - NN DDのみ実行
- `/deal:process_im [deal_name]` - IM DDのみ実行
- `/deal:extract_financials [deal_name]` - 財務諸表抽出のみ実行

## 使用方法
Cursorのチャットで `/` に続けてコマンド名を入力します。
