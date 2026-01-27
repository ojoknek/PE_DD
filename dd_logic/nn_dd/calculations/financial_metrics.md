# 財務指標計算ロジック - 数式仕様書

## 概要

本ドキュメントは、事業承継ファンド向けに拡張された財務指標計算のロジックを数式として記述した仕様書です。

## 1. 成長性指標

### 1.1 CAGR（年平均成長率）の計算

$$CAGR = \left[\left(\frac{End\ Value}{Start\ Value}\right)^{\frac{1}{Periods}} - 1\right] \times 100$$

ここで：
- $CAGR$: 年平均成長率（Compound Annual Growth Rate、%）
- $Start\ Value$: 開始値
- $End\ Value$: 終了値
- $Periods$: 期間数（年）

**計算条件**:
- $Start\ Value \leq 0$ または $Periods \leq 0$ の場合、$CAGR = 0$

**計算例**:
- 開始値: 450百万円
- 終了値: 600百万円
- 期間: 3年

$$CAGR = \left[\left(\frac{600}{450}\right)^{\frac{1}{3}} - 1\right] \times 100 = \left[1.333^{\frac{1}{3}} - 1\right] \times 100 \approx 10.06\%$$

## 2. 収益性指標

### 2.1 EBITDAマージンの計算

$$EBITDA\ Margin = \frac{EBITDA}{Revenue} \times 100$$

ここで：
- $EBITDA\ Margin$: EBITDAマージン（%）
- $EBITDA$: 税引前・金利前・減価償却前利益
- $Revenue$: 売上高

**計算条件**:
- $Revenue = 0$ の場合、$EBITDA\ Margin = 0$

### 2.2 営業利益率の計算

$$Operating\ Margin = \frac{Operating\ Income}{Revenue} \times 100$$

ここで：
- $Operating\ Margin$: 営業利益率（%）
- $Operating\ Income$: 営業利益
- $Revenue$: 売上高

**計算条件**:
- $Revenue = 0$ の場合、$Operating\ Margin = 0$

### 2.3 ROE（自己資本利益率）の計算

$$ROE = \frac{Net\ Income}{Equity} \times 100$$

ここで：
- $ROE$: 自己資本利益率（Return on Equity、%）
- $Net\ Income$: 当期純利益
- $Equity$: 自己資本

**計算条件**:
- $Equity = 0$ の場合、$ROE = 0$

### 2.4 ROA（総資産利益率）の計算

$$ROA = \frac{Net\ Income}{Total\ Assets} \times 100$$

ここで：
- $ROA$: 総資産利益率（Return on Assets、%）
- $Net\ Income$: 当期純利益
- $Total\ Assets$: 総資産

**計算条件**:
- $Total\ Assets = 0$ の場合、$ROA = 0$

## 3. 財務健全性指標

### 3.1 負債資本比率（Debt-to-Equity Ratio）の計算

$$Debt\ to\ Equity\ Ratio = \frac{Total\ Debt}{Equity} \times 100$$

ここで：
- $Debt\ to\ Equity\ Ratio$: 負債資本比率（%）
- $Total\ Debt$: 総負債
- $Equity$: 自己資本

**計算条件**:
- $Equity = null$ または $Equity = 0$ の場合、$Debt\ to\ Equity\ Ratio = null$（計算不能）
- $Total\ Debt = null$ の場合、$Total\ Debt = 0$ として扱う

### 3.2 流動比率の計算

$$Current\ Ratio = \frac{Current\ Assets}{Current\ Liabilities}$$

ここで：
- $Current\ Ratio$: 流動比率
- $Current\ Assets$: 流動資産
- $Current\ Liabilities$: 流動負債

**計算条件**:
- $Current\ Liabilities = null$ または $Current\ Liabilities = 0$ の場合、$Current\ Ratio = null$（計算不能）
- $Current\ Assets = null$ の場合、$Current\ Assets = 0$ として扱う

### 3.3 当座比率の計算

$$Quick\ Ratio = \frac{Current\ Assets - Inventory}{Current\ Liabilities}$$

ここで：
- $Quick\ Ratio$: 当座比率
- $Current\ Assets$: 流動資産
- $Inventory$: 在庫
- $Current\ Liabilities$: 流動負債

**計算条件**:
- $Current\ Liabilities = null$ または $Current\ Liabilities = 0$ の場合、$Quick\ Ratio = null$（計算不能）
- $Current\ Assets = null$ の場合、$Current\ Assets = 0$ として扱う
- $Inventory = null$ の場合、$Inventory = 0$ として扱う

## 4. 運転資金関連指標

### 4.1 運転資金の計算

$$Working\ Capital = Current\ Assets - Current\ Liabilities$$

ここで：
- $Working\ Capital$: 運転資金
- $Current\ Assets$: 流動資産
- $Current\ Liabilities$: 流動負債

**計算条件**:
- $Current\ Assets = null$ または $Current\ Liabilities = null$ の場合、$Working\ Capital = null$（計算不能）

### 4.2 運転資金回転率の計算

$$Working\ Capital\ Turnover = \frac{Revenue}{Working\ Capital}$$

ここで：
- $Working\ Capital\ Turnover$: 運転資金回転率
- $Revenue$: 売上高
- $Working\ Capital$: 運転資金

**計算条件**:
- $Working\ Capital = null$ または $Working\ Capital = 0$ の場合、$Working\ Capital\ Turnover = null$（計算不能）
- $Revenue = null$ の場合、$Working\ Capital\ Turnover = null$（計算不能）

## 5. 包括的財務指標の一括計算

### 5.1 計算プロセス

包括的財務指標を一括計算する場合、以下の順序で計算を実行します：

1. **基本指標の計算**
   - CAGR（売上高履歴がある場合）
   - EBITDAマージン
   - 営業利益率
   - ROE
   - ROA

2. **財務健全性指標の計算**
   - 負債資本比率
   - 流動比率
   - 当座比率

3. **運転資金関連指標の計算**
   - 運転資金
   - 運転資金回転率（運転資金が計算可能な場合）

### 5.2 入力データの要件

包括的財務指標計算に必要な入力データ：

| 項目 | 必須 | 説明 |
|------|------|------|
| revenue | 任意 | 売上高 |
| revenue_history | 任意 | 売上高の履歴（リスト） |
| ebitda | 任意 | EBITDA |
| operating_income | 任意 | 営業利益 |
| net_income | 任意 | 当期純利益 |
| equity | 任意 | 自己資本 |
| total_assets | 任意 | 総資産 |
| total_debt | 任意 | 総負債 |
| current_assets | 任意 | 流動資産 |
| current_liabilities | 任意 | 流動負債 |
| inventory | 任意 | 在庫 |

### 5.3 計算結果の構造

計算結果は以下の構造で返されます：

```json
{
  "cagr": 10.06,
  "ebitda_margin": 20.0,
  "operating_margin": 16.67,
  "roe": 15.0,
  "roa": 7.5,
  "debt_to_equity_ratio": 100.0,
  "current_ratio": 1.33,
  "quick_ratio": 1.0,
  "working_capital": 50,
  "working_capital_turnover": 12.0
}
```

## 6. 計算例

### 6.1 入力データ例

```json
{
  "revenue": 600,
  "revenue_history": [450, 500, 550, 600],
  "ebitda": 120,
  "operating_income": 100,
  "net_income": 60,
  "equity": 400,
  "total_assets": 800,
  "total_debt": 400,
  "current_assets": 200,
  "current_liabilities": 150,
  "inventory": 50
}
```

### 6.2 計算結果例

#### CAGR

$$CAGR = \left[\left(\frac{600}{450}\right)^{\frac{1}{3}} - 1\right] \times 100 \approx 10.06\%$$

#### EBITDAマージン

$$EBITDA\ Margin = \frac{120}{600} \times 100 = 20.0\%$$

#### 営業利益率

$$Operating\ Margin = \frac{100}{600} \times 100 \approx 16.67\%$$

#### ROE

$$ROE = \frac{60}{400} \times 100 = 15.0\%$$

#### ROA

$$ROA = \frac{60}{800} \times 100 = 7.5\%$$

#### 負債資本比率

$$Debt\ to\ Equity\ Ratio = \frac{400}{400} \times 100 = 100.0\%$$

#### 流動比率

$$Current\ Ratio = \frac{200}{150} \approx 1.33$$

#### 当座比率

$$Quick\ Ratio = \frac{200 - 50}{150} = 1.0$$

#### 運転資金

$$Working\ Capital = 200 - 150 = 50$$

#### 運転資金回転率

$$Working\ Capital\ Turnover = \frac{600}{50} = 12.0$$
