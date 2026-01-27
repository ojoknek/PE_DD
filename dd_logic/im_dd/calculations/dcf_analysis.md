# DCF（Discounted Cash Flow）分析 - 数式仕様書

## 概要

本ドキュメントは、IM DD評価におけるDCF分析の計算ロジックを数式として記述した仕様書です。参考文献「壁の道の向こう側」のDCF法・財務モデリング手法に基づいています。

## 1. アンレバード・フリー・キャッシュフロー（FCF）の計算

### 1.1 EBITDAの定義

EBITDAは以下の3つのCを満たす必要があります：

- **Core**: その会社の本業からの収益であること
- **Continuing**: その事業が継続していること
- **Controlled**: その事業を支配していること

### 1.2 FCF計算プロセス

アンレバード・フリー・キャッシュフロー（FCF）は以下の計算プロセスで算出されます：

#### ステップ1: EBITの計算

$$EBIT = EBITDA - Depreciation$$

ここで：
- $EBIT$: 営業利益（Earnings Before Interest and Tax）
- $EBITDA$: 税引前・金利前・減価償却前利益
- $Depreciation$: 減価償却費

#### ステップ2: NOPATの計算

$$NOPAT = EBIT \times (1 - T)$$

ここで：
- $NOPAT$: 本業の税引後利益（Net Operating Profit After Tax）
- $T$: 実効税率（Tax Rate）

#### ステップ3: FCFの計算

$$FCF = NOPAT + Depreciation - \Delta WC - Capex - \Delta ONCA - \Delta DTL$$

ここで：
- $FCF$: アンレバード・フリー・キャッシュフロー（Free Cash Flow）
- $\Delta WC$: 運転資本の変化額（Working Capital Change）
- $Capex$: 設備投資額（Capital Expenditure）
- $\Delta ONCA$: その他非流動資産の変化額（Other Non-Current Assets Change）
- $\Delta DTL$: 繰延税金負債の変化額（Deferred Tax Liability Change）

### 1.3 予測期間

- 一般的に5〜10年先まで予測
- 企業の成長段階や業種によって調整

## 2. WACC（加重平均資本コスト）の計算

### 2.1 WACC基本式

$$WACC = \frac{E}{D + E} \times K_e + \frac{D}{D + E} \times K_d \times (1 - T)$$

ここで：
- $WACC$: 加重平均資本コスト（Weighted Average Cost of Capital）
- $E$: 株式価値（Equity Value）
- $D$: 負債価値（Debt Value）
- $K_e$: 株主資本コスト（Cost of Equity）
- $K_d$: 負債資本コスト（Cost of Debt）
- $T$: 実効税率（Tax Rate）

### 2.2 株主資本コスト（$K_e$）の計算（CAPMモデル）

$$K_e = R_f + \beta_{lev} \times (R_m - R_f)$$

ここで：
- $K_e$: 株主資本コスト（Cost of Equity）
- $R_f$: リスクフリーレート（Risk-Free Rate、長期国債の利回り）
- $\beta_{lev}$: レバードベータ（Levered Beta）
- $R_m$: マーケットリターン（Market Return）
- $(R_m - R_f)$: マーケットリスクプレミアム（Market Risk Premium）

### 2.3 ベータのアンレバリング

類似企業のレバードベータをアンレバリングして、無借金状態のベータに変換します：

$$\beta_U = \frac{\beta_{lev}}{1 + \frac{D}{E} \times (1 - T)}$$

ここで：
- $\beta_U$: アンレバードベータ（Unlevered Beta）
- $\beta_{lev}$: レバードベータ（Levered Beta）
- $\frac{D}{E}$: 負債/株式比率（Debt-to-Equity Ratio）
- $T$: 実効税率（Tax Rate）

### 2.4 ベータのリレバリング

アンレバードベータを対象企業の負債比率に応じてリレバリングします：

$$\beta_{lev} = \beta_U \times \left[1 + \frac{D}{E} \times (1 - T)\right]$$

### 2.5 修正ベータの計算

ベータは最終的には市場平均である1に収斂するという考え方に基づき、修正ベータを計算します：

$$\beta_{adjusted} = \beta_{unadjusted} \times \frac{2}{3} + \frac{1}{3}$$

ここで：
- $\beta_{adjusted}$: 修正ベータ（Adjusted Beta）
- $\beta_{unadjusted}$: 未修正ベータ（Unadjusted Beta）

### 2.6 WACC詳細計算

WACCの各構成要素を詳細に計算します：

#### 株式ウェイト

$$w_e = \frac{E}{D + E}$$

#### 負債ウェイト

$$w_d = \frac{D}{D + E}$$

#### 株式コスト構成要素

$$C_e = w_e \times K_e$$

#### 負債コスト構成要素

$$C_d = w_d \times K_d \times (1 - T)$$

#### WACC

$$WACC = C_e + C_d$$

## 3. ターミナル・バリューの計算（Gordon Growth Model）

$$TV = \frac{FCF_{final} \times (1 + g)}{WACC - g}$$

ここで：
- $TV$: ターミナル・バリュー（Terminal Value）
- $FCF_{final}$: 最終年度のフリーキャッシュフロー
- $g$: ターミナル成長率（Terminal Growth Rate、一般的に2-3%）
- $WACC$: 加重平均資本コスト

**注意**: $WACC \leq g$ の場合は、ターミナル・バリューは計算不能（0を返す）

## 4. DCF分析の実行

### 4.1 予測期間のFCFの現在価値

各年度のFCFを現在価値に割り引きます：

$$PV_{FCF,t} = \frac{FCF_t}{(1 + WACC)^t}$$

ここで：
- $PV_{FCF,t}$: 年度$t$のFCFの現在価値（Present Value of FCF at period $t$）
- $FCF_t$: 年度$t$のフリーキャッシュフロー
- $WACC$: 加重平均資本コスト
- $t$: 年度（1, 2, 3, ...）

### 4.2 予測期間のFCFの現在価値合計

$$PV_{FCF} = \sum_{t=1}^{n} PV_{FCF,t} = \sum_{t=1}^{n} \frac{FCF_t}{(1 + WACC)^t}$$

ここで：
- $PV_{FCF}$: 予測期間のFCFの現在価値合計
- $n$: 予測期間の年数

### 4.3 ターミナル・バリューの現在価値

$$PV_{TV} = \frac{TV}{(1 + WACC)^n}$$

ここで：
- $PV_{TV}$: ターミナル・バリューの現在価値（Present Value of Terminal Value）
- $TV$: ターミナル・バリュー
- $n$: 予測期間の年数

### 4.4 企業価値（EV）の計算

$$EV = PV_{FCF} + PV_{TV}$$

ここで：
- $EV$: 企業価値（Enterprise Value）

## 5. 企業価値（EV）から株式価値への変換

$$Equity\ Value = EV - Net\ Debt + Non\ Operating\ Assets - Minority\ Interest$$

ここで：
- $Equity\ Value$: 株式価値（株主価値）
- $EV$: 企業価値（Enterprise Value）
- $Net\ Debt$: 純有利子負債（有利子負債 - 現預金）
- $Non\ Operating\ Assets$: 本業以外の資産価値
- $Minority\ Interest$: 少数株主持分

## 6. 感度分析

### 6.1 感度分析の考え方

複数の変数（割引率、成長率等）を変化させて、企業価値への影響を分析します。

### 6.2 感度分析の計算

割引率の範囲 $[WACC_{min}, WACC_{max}]$ と成長率の範囲 $[g_{min}, g_{max}]$ を設定し、各組み合わせでDCF分析を実行します：

$$EV_{i,j} = DCF(WACC_i, g_j, FCF_{base}, TV_{base})$$

ここで：
- $EV_{i,j}$: 割引率$WACC_i$、成長率$g_j$での企業価値
- $FCF_{base}$: ベースケースのフリーキャッシュフロー
- $TV_{base}$: ベースケースのターミナル・バリュー

### 6.3 フットボールチャート

感度分析の結果を表形式（フットボールチャート）で可視化します。

## 7. シナリオ分析

### 7.1 ベースケース

最も確からしい予測に基づくDCF分析：

$$EV_{base} = DCF(FCF_{base}, WACC_{base}, g_{base})$$

### 7.2 楽観ケース

成長率やマージンが高めの予測に基づくDCF分析：

$$EV_{optimistic} = DCF(FCF_{optimistic}, WACC_{base}, g_{base})$$

### 7.3 悲観ケース

成長率やマージンが低めの予測に基づくDCF分析：

$$EV_{pessimistic} = DCF(FCF_{pessimistic}, WACC_{base}, g_{base})$$

## 8. 計算例

### 8.1 入力データ例

- 予測期間: 5年
- 各年度のFCF: [100, 120, 140, 160, 180]（百万円）
- WACC: 10%（0.10）
- ターミナル成長率: 3%（0.03）

### 8.2 計算プロセス

#### ステップ1: 各年度のFCFの現在価値

$$PV_{FCF,1} = \frac{100}{(1 + 0.10)^1} = 90.91$$

$$PV_{FCF,2} = \frac{120}{(1 + 0.10)^2} = 99.17$$

$$PV_{FCF,3} = \frac{140}{(1 + 0.10)^3} = 105.18$$

$$PV_{FCF,4} = \frac{160}{(1 + 0.10)^4} = 109.28$$

$$PV_{FCF,5} = \frac{180}{(1 + 0.10)^5} = 111.69$$

#### ステップ2: 予測期間のFCFの現在価値合計

$$PV_{FCF} = 90.91 + 99.17 + 105.18 + 109.28 + 111.69 = 516.23$$

#### ステップ3: ターミナル・バリューの計算

$$TV = \frac{180 \times (1 + 0.03)}{0.10 - 0.03} = \frac{185.4}{0.07} = 2,648.57$$

#### ステップ4: ターミナル・バリューの現在価値

$$PV_{TV} = \frac{2,648.57}{(1 + 0.10)^5} = 1,643.13$$

#### ステップ5: 企業価値（EV）の計算

$$EV = 516.23 + 1,643.13 = 2,159.36$$

## 参考文献

- `dd_logic/references/web/壁の道の向こう側/` - DCF法・財務モデリングの詳細な解説
  - オペレーティングモデル構築の12ステップ
  - FCF計算方法
  - WACC計算方法
  - ターミナル・バリュー計算方法
