# LBOモデル構築 - 数式仕様書

## 概要

本ドキュメントは、LBO（Leveraged Buyout）モデルを構築するための計算ロジックを数式として記述した仕様書です。参考文献「壁の道の向こう側」のLBOモデル作成手法に基づいています。

LBOモデルは、レバレッジド・バイアウトの実行判断を行うための財務モデルであり、以下の要素を含みます：
- レバレッジ比率の設定
- 負債スケジュールの構築（キャッシュスイープ付き）
- エクイティ・コントリビューションの計算
- IRR（内部収益率）の計算
- MOIC（Multiple of Invested Capital）の計算
- 安全性分析
- 売却時のEVと株式価値の計算

## 1. LBOモデル構築の基本フロー

### 1.1 データソース

LBOモデル構築に必要なデータは、以下のディレクトリから取得します：
- **VDR資料**: `deals/[deal_name]/vdr/im/` - IM関連VDR資料
- **財務諸表**: VDR資料から抽出した財務諸表データ

### 1.2 構築ステップ（18ステップ）

参考文献に基づくLBOモデル構築の18ステップ：

1. エクセルの反復計算をオフにする
2. 損益計算書（IS）を構築する（減価償却、受取・支払利息は空欄のまま）
3. 設備投資や資本等（mixed account）と運転資本を計算し、減価償却をISにリンクさせる
4. 負債の返済スケジュールと受取・支払利息を計算する（手数料と償却スケジュールの設定）
5. 貸借対照表（BS）を構築する（現金と短期借入金は除く）
6. BSの各項目をキャッシュフロー計算書（CF）の項目毎に分類する
7. CFを構築する（EBITDAベースで営業CFを構築）
8. CFで算出した現金/短期借入金をBSにリンクさせる
9. 受取・支払利息をISにリンクさせる（循環参照発生）
10. エクセルの反復計算をオンにする
11. 循環参照のオン・オフができるスイッチを構築する
12. 期末の負債残高をBSにリンクさせ、BSの負債残高前年比をCFにリンクさせる
13. キャッシュスイープのついた負債の返済スケジュールと受取・支払利息を計算する
14. 期末の負債残高をBSにリンクさせ、BSの負債残高前年比をCFにリンクさせる
15. 受取・支払利息をISにリンクさせる（循環参照発生）
16. 安全性分析を行う
17. 売却時のEnterprise value（EV）と株式価値を計算する
18. 収益率と感応度の分析を行う

## 2. レバレッジ比率の設定

### 2.1 買収価格の計算

$$Purchase\ Price = Equity\ Value + Net\ Debt$$

ここで：
- $Purchase\ Price$: 買収価格
- $Equity\ Value$: 株式価値（買収時の評価）
- $Net\ Debt$: 純有利子負債（有利子負債 - 現預金）

### 2.2 レバレッジ比率の設定

$$Leverage\ Ratio = \frac{Total\ Debt}{Equity\ Contribution}$$

ここで：
- $Leverage\ Ratio$: レバレッジ比率
- $Total\ Debt$: 総負債額
- $Equity\ Contribution$: エクイティ・コントリビューション（投資家が出資する株式）

### 2.3 負債構成の設定

LBOモデルでは、通常以下の負債種類を使用します：
- **タームローンA（Term Loan A）**: 優先順位の高い負債
- **タームローンB（Term Loan B）**: 優先順位がやや低い負債
- **ハイイールド債（High Yield Bond）**: 劣後的な負債

$$Total\ Debt = Term\ Loan\ A + Term\ Loan\ B + High\ Yield\ Bond$$

## 3. 負債スケジュールの構築

### 3.1 負債の返済スケジュール

各負債種類について、返済スケジュールを設定します：

$$Debt\ Balance_{t} = Debt\ Balance_{t-1} - Scheduled\ Repayment_t - Cash\ Sweep_t$$

ここで：
- $Debt\ Balance_{t}$: 年度$t$の負債残高
- $Debt\ Balance_{t-1}$: 前年度の負債残高
- $Scheduled\ Repayment_t$: 年度$t$の予定返済額
- $Cash\ Sweep_t$: 年度$t$のキャッシュスイープ返済額

### 3.2 キャッシュスイープ（Cash Sweep）

余剰資金を負債の返済に強制的に充当する仕組み：

$$Available\ Cash_{t} = Beginning\ Cash_{t} + Operating\ CF_{t} - Minimum\ Cash_{t}$$

$$Cash\ Sweep_{t} = \min(Available\ Cash_{t}, Remaining\ Debt_{t})$$

ここで：
- $Available\ Cash_{t}$: 年度$t$の利用可能現金
- $Beginning\ Cash_{t}$: 年度$t$の期首現金
- $Operating\ CF_{t}$: 年度$t$の営業キャッシュフロー
- $Minimum\ Cash_{t}$: 年度$t$の最低必要現金（ミニマムキャッシュ）
- $Remaining\ Debt_{t}$: 年度$t$の残存負債額

### 3.3 負債返済の優先順位

キャッシュスイープは、通常以下の優先順位で返済されます：
1. タームローンA
2. タームローンB
3. ハイイールド債

## 4. 支払利息の計算

### 4.1 固定金利の場合

$$Interest\ Payment_{t} = Debt\ Balance_{t-1} \times Interest\ Rate$$

ここで：
- $Interest\ Payment_{t}$: 年度$t$の支払利息
- $Debt\ Balance_{t-1}$: 前年度の負債残高
- $Interest\ Rate$: 金利（固定）

### 4.2 変動金利の場合

$$Interest\ Payment_{t} = Debt\ Balance_{t-1} \times (Base\ Rate_{t} + Spread)$$

ここで：
- $Base\ Rate_{t}$: 年度$t$の基準金利（LIBOR、SOFR等）
- $Spread$: スプレッド（固定）

## 5. エクイティ・コントリビューションの計算

### 5.1 エクイティ・コントリビューション

$$Equity\ Contribution = Purchase\ Price - Total\ Debt$$

ここで：
- $Equity\ Contribution$: エクイティ・コントリビューション（投資家が出資する株式）
- $Purchase\ Price$: 買収価格
- $Total\ Debt$: 総負債額

### 5.2 エクイティ・コントリビューション比率

$$Equity\ Ratio = \frac{Equity\ Contribution}{Purchase\ Price}$$

## 6. IRR（内部収益率）の計算

### 6.1 IRRの定義

IRRは、投資期間中のキャッシュフローの現在価値の合計がゼロになる割引率です：

$$\sum_{t=0}^{n} \frac{CF_t}{(1 + IRR)^t} = 0$$

ここで：
- $IRR$: 内部収益率（Internal Rate of Return）
- $CF_t$: 年度$t$のキャッシュフロー
- $n$: 投資期間（年数）

### 6.2 LBO投資におけるキャッシュフロー

LBO投資におけるキャッシュフロー：
- **初期投資（$t=0$）**: エクイティ・コントリビューション（負の値）
- **中間年度（$t=1$ 〜 $n-1$）**: 配当等のキャッシュフロー（通常は0）
- **最終年度（$t=n$）**: 売却時の株式価値（正の値）

$$CF_0 = -Equity\ Contribution$$

$$CF_t = 0 \quad (t = 1, 2, ..., n-1)$$

$$CF_n = Exit\ Equity\ Value$$

### 6.3 IRRの計算

IRRは、以下の方程式を解くことで求められます：

$$-Equity\ Contribution + \frac{Exit\ Equity\ Value}{(1 + IRR)^n} = 0$$

これを変形すると：

$$IRR = \left(\frac{Exit\ Equity\ Value}{Equity\ Contribution}\right)^{\frac{1}{n}} - 1$$

## 7. MOIC（Multiple of Invested Capital）の計算

### 7.1 MOICの定義

$$MOIC = \frac{Exit\ Equity\ Value}{Equity\ Contribution}$$

ここで：
- $MOIC$: Multiple of Invested Capital（投資資本倍率）
- $Exit\ Equity\ Value$: 売却時の株式価値
- $Equity\ Contribution$: エクイティ・コントリビューション（初期投資額）

### 7.2 MOICとIRRの関係

$$MOIC = (1 + IRR)^n$$

ここで：
- $n$: 投資期間（年数）

## 8. 安全性分析

### 8.1 レバレッジレシオ（Leverage Ratio）

$$Leverage\ Ratio = \frac{Total\ Debt}{EBITDA}$$

ここで：
- $Total\ Debt$: 総有利子負債
- $EBITDA$: 税引前・金利前・減価償却前利益

### 8.2 インタレストカバレッジレシオ（Interest Coverage Ratio）

$$Interest\ Coverage\ Ratio = \frac{EBIT}{Interest\ Expense}$$

ここで：
- $EBIT$: 営業利益（Earnings Before Interest and Tax）
- $Interest\ Expense$: 支払利息

### 8.3 デットサービスカバレッジレシオ（Debt Service Coverage Ratio）

$$DSCR = \frac{EBITDA}{Interest\ Expense + Principal\ Repayment}$$

ここで：
- $DSCR$: Debt Service Coverage Ratio
- $Principal\ Repayment$: 元本返済額

### 8.4 コベナンツ（財務制限条項）のチェック

金融機関が設定する主なコベナンツ：
- **最大レバレッジレシオ**: $Leverage\ Ratio \leq Threshold$
- **最小インタレストカバレッジレシオ**: $Interest\ Coverage\ Ratio \geq Threshold$
- **最小DSCR**: $DSCR \geq Threshold$

## 9. 売却時のEVと株式価値の計算

### 9.1 売却時のEVの計算

$$Exit\ EV = Exit\ EBITDA \times EV/EBITDA\ Multiple$$

ここで：
- $Exit\ EV$: 売却時の企業価値（Enterprise Value）
- $Exit\ EBITDA$: 売却時のEBITDA
- $EV/EBITDA\ Multiple$: EV/EBITDA倍率（通常は買収時の倍率を使用）

### 9.2 売却時の株式価値の計算

$$Exit\ Equity\ Value = Exit\ EV - Exit\ Net\ Debt + Non\ Operating\ Assets - Minority\ Interest$$

ここで：
- $Exit\ Equity\ Value$: 売却時の株式価値
- $Exit\ EV$: 売却時の企業価値
- $Exit\ Net\ Debt$: 売却時の純有利子負債
- $Non\ Operating\ Assets$: 本業以外の資産価値
- $Minority\ Interest$: 少数株主持分

### 9.3 PEファンドの持分比率

売却時のPEファンドの持分比率を考慮：

$$PE\ Fund\ Exit\ Value = Exit\ Equity\ Value \times Ownership\ Percentage$$

ここで：
- $PE\ Fund\ Exit\ Value$: PEファンドの売却時価値
- $Ownership\ Percentage$: PEファンドの持分比率（経営陣へのインセンティブ配布を考慮）

## 10. 年別リターンシミュレーション

### 10.1 各年度での売却を想定したIRR計算

各年度$t$での売却を想定したIRR：

$$IRR_t = \left(\frac{Exit\ Equity\ Value_t}{Equity\ Contribution}\right)^{\frac{1}{t}} - 1$$

### 10.2 各年度での売却を想定したMOIC計算

$$MOIC_t = \frac{Exit\ Equity\ Value_t}{Equity\ Contribution}$$

## 11. 感応度分析（Sensitivity Analysis）

### 11.1 買収プレミアムの変化による影響

買収プレミアムを変化させた場合のIRR：

$$IRR_{premium} = f(Purchase\ Price_{premium}, Exit\ Equity\ Value)$$

ここで：
- $Purchase\ Price_{premium}$: プレミアムを考慮した買収価格
- $Exit\ Equity\ Value$: 売却時の株式価値（固定）

### 11.2 売却倍率の変化による影響

売却時のEV/EBITDA倍率を変化させた場合のIRR：

$$IRR_{multiple} = f(Equity\ Contribution, Exit\ EV_{multiple})$$

ここで：
- $Exit\ EV_{multiple}$: 倍率を変化させた売却時のEV

### 11.3 感応度分析の実施

複数の変数を組み合わせて感応度分析を実施：
- 買収プレミアム × 売却倍率
- 買収プレミアム × 売却年度
- 売却倍率 × 売却年度

## 12. 営業キャッシュフローの構築（EBITDAベース）

### 12.1 EBITDAベースの営業CF

LBOモデルでは、営業キャッシュフローをEBITDAベースで構築します：

$$Operating\ CF = EBITDA - Taxes - \Delta WC - Other\ Adjustments$$

ここで：
- $Operating\ CF$: 営業キャッシュフロー
- $EBITDA$: 税引前・金利前・減価償却前利益
- $Taxes$: 税金（EBITベース）
- $\Delta WC$: 運転資本の変化額
- $Other\ Adjustments$: その他の調整項目

### 12.2 EBITDAベースの利点

EBITDAベースで営業CFを構築することで、支払利息をCF計算上で表示でき、LBO投資における負債返済の見通しが明確になります。

## 13. ミニマムキャッシュ（Minimum Cash）の設定

### 13.1 ミニマムキャッシュの定義

企業が最低限保持すべき現金残高：

$$Minimum\ Cash_{t} = Revenue_{t} \times Minimum\ Cash\ Ratio$$

または固定額：

$$Minimum\ Cash_{t} = Fixed\ Amount$$

### 13.2 ミニマムキャッシュの目的

- 運転資金の確保
- 予期しない支出への対応
- 金融機関との契約条件

## 14. 計算例

### 14.1 入力データ例

- 買収価格: 2,000百万円
- エクイティ・コントリビューション: 500百万円
- 総負債: 1,500百万円
  - タームローンA: 800百万円（金利3%）
  - タームローンB: 500百万円（金利4%）
  - ハイイールド債: 200百万円（金利6%）
- 投資期間: 5年
- 売却時のEBITDA: 300百万円
- 売却時のEV/EBITDA倍率: 6.0倍
- 売却時のNet Debt: 800百万円

### 14.2 計算プロセス

#### ステップ1: 売却時のEVの計算

$$Exit\ EV = 300 \times 6.0 = 1,800\ 百万円$$

#### ステップ2: 売却時の株式価値の計算

$$Exit\ Equity\ Value = 1,800 - 800 = 1,000\ 百万円$$

#### ステップ3: MOICの計算

$$MOIC = \frac{1,000}{500} = 2.0\ 倍$$

#### ステップ4: IRRの計算

$$IRR = \left(\frac{1,000}{500}\right)^{\frac{1}{5}} - 1 = 2.0^{0.2} - 1 \approx 0.149 = 14.9\%$$

## 15. 出力形式

LBOモデルの構築結果は、以下の形式で `deals/[deal_name]/ai_dd_results/lbo_dd/` に保存されます：

- `report.md`: LBO DD結果レポート（実行判断を含む）
- レポートには以下を含む：
  - レバレッジ比率
  - 負債スケジュール
  - エクイティ・コントリビューション
  - IRR・MOIC
  - 安全性分析結果
  - 売却時のEVと株式価値
  - 感応度分析結果
  - 実行判断の推奨

## 参考文献

- `dd_logic/references/web/壁の道の向こう側/` - LBOモデル作成の詳細な解説
  - 投資銀行の本格的LBOモデル作成方法（12ステップ）
  - キャッシュスイープモデルの構築方法
  - 安全性分析の実施方法
  - 売却時のEVと株式価値の計算方法
