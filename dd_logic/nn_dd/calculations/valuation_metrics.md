# バリュエーション指標計算ロジック - 数式仕様書

## 概要

本ドキュメントは、NN DD評価に必要なバリュエーション指標の計算ロジックを数式として記述した仕様書です。

## 1. Net Debt（純有利子負債）の計算

### 1.1 計算式

$$Net\ Debt = Interest\ Bearing\ Debt - Cash\ and\ Equivalents$$

ここで：
- $Net\ Debt$: 純有利子負債（Net Debt）
- $Interest\ Bearing\ Debt$: 有利子負債
- $Cash\ and\ Equivalents$: 現預金

### 1.2 計算条件

- $Interest\ Bearing\ Debt = null$ の場合、$Net\ Debt = null$（計算不能）
- $Cash\ and\ Equivalents = null$ の場合、$Cash\ and\ Equivalents = 0$ として扱う

### 1.3 計算例

- 有利子負債: 400百万円
- 現預金: 100百万円

$$Net\ Debt = 400 - 100 = 300\ 百万円$$

## 2. 企業価値（EV）の計算

### 2.1 EBITDA倍率からの計算

$$EV = Adj\ EBITDA \times EBITDA\ Multiple$$

ここで：
- $EV$: 企業価値（Enterprise Value）
- $Adj\ EBITDA$: 調整後EBITDA
- $EBITDA\ Multiple$: EBITDA倍率

### 2.2 計算条件

- $Adj\ EBITDA = null$ または $EBITDA\ Multiple = null$ の場合、$EV = null$（計算不能）

### 2.3 計算例

- 調整後EBITDA: 120百万円
- EBITDA倍率: 4.0倍

$$EV = 120 \times 4.0 = 480\ 百万円$$

## 3. 株主価値（Equity Value）の計算

### 3.1 企業価値からの計算

$$Equity\ Value = EV - Net\ Debt$$

ここで：
- $Equity\ Value$: 株主価値（Equity Value）
- $EV$: 企業価値（Enterprise Value）
- $Net\ Debt$: 純有利子負債（未入力の場合は0として扱う）

### 3.2 計算条件

- $EV = null$ の場合、$Equity\ Value = null$（計算不能）
- $Net\ Debt = null$ の場合、$Net\ Debt = 0$ として扱う

### 3.3 計算例

- 企業価値（EV）: 480百万円
- Net Debt: 300百万円

$$Equity\ Value = 480 - 300 = 180\ 百万円$$

## 4. 計算プロセスの全体フロー

### 4.1 ステップ1: Net Debtの計算

$$Net\ Debt = Interest\ Bearing\ Debt - Cash\ and\ Equivalents$$

### 4.2 ステップ2: EVの計算

$$EV = Adj\ EBITDA \times EBITDA\ Multiple$$

### 4.3 ステップ3: Equity Valueの計算

$$Equity\ Value = EV - Net\ Debt$$

## 5. 統合計算例

### 5.1 入力データ例

- 有利子負債: 400百万円
- 現預金: 100百万円
- 調整後EBITDA: 120百万円
- EBITDA倍率: 4.0倍

### 5.2 計算プロセス

#### ステップ1: Net Debtの計算

$$Net\ Debt = 400 - 100 = 300\ 百万円$$

#### ステップ2: EVの計算

$$EV = 120 \times 4.0 = 480\ 百万円$$

#### ステップ3: Equity Valueの計算

$$Equity\ Value = 480 - 300 = 180\ 百万円$$

### 5.3 計算結果

- Net Debt: 300百万円
- EV: 480百万円
- Equity Value: 180百万円

## 6. 注意事項

### 6.1 未入力値の扱い

- 各計算において、未入力値（$null$）の扱いを明確に定義
- 計算不能な場合は $null$ を返す
- 一部の値が未入力でも計算可能な場合は、デフォルト値（0等）を使用

### 6.2 計算順序

- Net Debt → EV → Equity Value の順序で計算
- 前段階の計算結果が $null$ の場合、後続の計算も $null$ となる
