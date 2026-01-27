# NN DD計算ロジック - 数式仕様書

## 概要

本ドキュメントは、事業承継ファンド向けNN DD評価における計算ロジックを数式として記述した仕様書です。定量情報と定性情報を統合した結論導出ロジックを含みます。

## 1. 中間計算（Derived Metrics）

### 1.1 ND/EBITDA（レバレッジ）の計算

$$ND/EBITDA = \frac{Net\ Debt}{Adj\ EBITDA}$$

ここで：
- $ND/EBITDA$: ND/EBITDA倍率（レバレッジ）
- $Net\ Debt$: 純有利子負債（有利子負債 - 現預金）
- $Adj\ EBITDA$: 調整後EBITDA

**計算条件**:
- $Adj\ EBITDA = 0$ または未入力の場合、$ND/EBITDA = null$（計算不能）
- $Net\ Debt$ が未入力の場合、$ND/EBITDA = null$

### 1.2 EV（企業価値）の計算

$$EV = Adj\ EBITDA \times EBITDA\ Multiple$$

ここで：
- $EV$: 企業価値（Enterprise Value）
- $Adj\ EBITDA$: 調整後EBITDA
- $EBITDA\ Multiple$: EBITDA倍率

**計算条件**:
- $Adj\ EBITDA$ または $EBITDA\ Multiple$ が未入力の場合、$EV = null$

### 1.3 Equity Value（株主価値）の計算

$$Equity\ Value = EV - Net\ Debt$$

ここで：
- $Equity\ Value$: 株主価値（Equity Value）
- $EV$: 企業価値（Enterprise Value）
- $Net\ Debt$: 純有利子負債（未入力の場合は0として扱う）

**計算条件**:
- $EV = null$ の場合、$Equity\ Value = null$

### 1.4 定性合計の計算

$$Qual\ Total = Fit\ Score + Brand\ Score + Digital\ Score + Scarcity\ Score$$

ここで：
- $Qual\ Total$: 定性合計スコア（範囲: 4〜20点）
- $Fit\ Score$: 領域・業態適合度（1〜5点、未入力は0として扱う）
- $Brand\ Score$: ブランド・独自性（1〜5点、未入力は0として扱う）
- $Digital\ Score$: ファンベース・D2C（1〜5点、未入力は0として扱う）
- $Scarcity\ Score$: 特定分野・地域性（1〜5点、未入力は0として扱う）

## 2. 定量（財務）の離散判定（Discrete Ratings）

### 2.1 判定ランクの定義

| ランク | 記号 | 説明 |
|--------|------|------|
| EXCELLENT | ◎ | 優秀 |
| GOOD | 〇 | 良好 |
| WARNING | △ | 注意 |
| FAIL | × | 不合格 |
| NO_DATA | - | 数値未入力 |
| EMPTY | - | （空欄） |

### 2.2 売上高判定

| 条件 | 判定 |
|------|------|
| $sales = null$ | 数値未入力 |
| $sales \geq 500$ | 〇 |
| $300 \leq sales < 500$ | △ |
| $sales < 300$ | × |

ここで：
- $sales$: 売上高（百万円単位）

### 2.3 調整後EBITDA判定

| 条件 | 判定 |
|------|------|
| $adj\_ebitda = null$ | 数値未入力 |
| $adj\_ebitda \geq 100$ | ◎ |
| $50 \leq adj\_ebitda < 100$ | 〇 |
| $adj\_ebitda < 50$ | × |

ここで：
- $adj\_ebitda$: 調整後EBITDA（百万円単位）

### 2.4 ND/EBITDA判定

| 条件 | 判定 |
|------|------|
| $nd\_to\_ebitda = null$ | 数値未入力 |
| $nd\_to\_ebitda \leq 3$ | ◎ |
| $3 < nd\_to\_ebitda \leq 4$ | 〇 |
| $nd\_to\_ebitda > 4$ | × |

ここで：
- $nd\_to\_ebitda$: ND/EBITDA倍率

### 2.5 EBITDA倍率判定

| 条件 | 判定 |
|------|------|
| $ebitda\_multiple = null$ | 数値未入力 |
| $ebitda\_multiple \leq 3$ | ◎ |
| $3 < ebitda\_multiple \leq 4$ | 〇 |
| $ebitda\_multiple > 4$ | × |

ここで：
- $ebitda\_multiple$: EBITDA倍率

### 2.6 EV判定（参考：サイズ適合）

| 条件 | 判定 |
|------|------|
| $ev = null$ | （空欄） |
| $1000 \leq ev \leq 2500$ | 〇 |
| 上記以外 | △ |

ここで：
- $ev$: 企業価値（百万円単位）

**注意**: EVは×判定を持たない（ゲート要因にしない）

### 2.7 Equity Value判定（参考：サイズ適合）

| 条件 | 判定 |
|------|------|
| $equity\_value = null$ | 数値未入力 |
| $300 \leq equity\_value \leq 1500$ | 〇 |
| 上記以外 | △ |

ここで：
- $equity\_value$: 株主価値（百万円単位）

**注意**: Equity Valueは×判定を持たない（ゲート要因にしない）

## 3. 定量総合判定（Quant Gate）

### 3.1 判定ロジック

$$Quant\ Result = \begin{cases}
NG & \text{if } \exists rating \in \{sales, adj\_ebitda, nd\_to\_ebitda, ebitda\_multiple\} : rating = \times \\
OK & \text{otherwise}
\end{cases}$$

ここで：
- $Quant\ Result$: 定量総合判定結果（OK または NG）
- $rating$: 各定量指標の判定結果

### 3.2 判定対象

定量総合判定の対象となる指標：
- 売上高判定（$sales\_rating$）
- 調整後EBITDA判定（$adj\_ebitda\_rating$）
- ND/EBITDA判定（$nd\_to\_ebitda\_rating$）
- EBITDA倍率判定（$ebitda\_multiple\_rating$）

**注意**: EV判定とEquity Value判定は参考情報であり、ゲート判定の対象外

### 3.3 論理式による表現

$$Quant\ Result = \begin{cases}
NG & \text{if } (sales\_rating = \times) \lor (adj\_ebitda\_rating = \times) \lor (nd\_to\_ebitda\_rating = \times) \lor (ebitda\_multiple\_rating = \times) \\
OK & \text{otherwise}
\end{cases}$$

## 4. 定性判定（Qual Gate）

### 4.1 判定ロジック

$$Qual\ Passed = \begin{cases}
True & \text{if } Qual\ Total \geq 15 \\
False & \text{if } Qual\ Total < 15
\end{cases}$$

ここで：
- $Qual\ Passed$: 定性ゲート合格フラグ（True: 合格、False: 不合格）
- $Qual\ Total$: 定性合計スコア（4〜20点）
- 合格基準: 15点以上

## 5. 最終判定（見送り/見送りでない）

### 5.1 見送り条件（Skip）

$$Skip = (Quant\ Result = NG) \lor (Qual\ Total < 15)$$

論理式で表現すると：

$$Skip = (Quant\ Result = NG) \lor \neg Qual\ Passed$$

### 5.2 見送りでない条件（Pass）

$$Pass = (Quant\ Result = OK) \land (Qual\ Total \geq 15)$$

論理式で表現すると：

$$Pass = (Quant\ Result = OK) \land Qual\ Passed$$

### 5.3 最終判定の決定

$$Final\ Decision = \begin{cases}
見送り & \text{if } Skip \\
見送りでない & \text{if } Pass
\end{cases}$$

## 6. 計算プロセスの全体フロー

### 6.1 ステップ1: 中間計算

1. $ND/EBITDA = \frac{Net\ Debt}{Adj\ EBITDA}$ を計算
2. $EV = Adj\ EBITDA \times EBITDA\ Multiple$ を計算
3. $Equity\ Value = EV - Net\ Debt$ を計算
4. $Qual\ Total = Fit\ Score + Brand\ Score + Digital\ Score + Scarcity\ Score$ を計算

### 6.2 ステップ2: 定量判定

各指標について離散判定を実行：
- 売上高判定
- 調整後EBITDA判定
- ND/EBITDA判定
- EBITDA倍率判定
- EV判定（参考）
- Equity Value判定（参考）

### 6.3 ステップ3: 定量総合判定

$$Quant\ Result = \begin{cases}
NG & \text{if } \exists rating = \times \\
OK & \text{otherwise}
\end{cases}$$

### 6.4 ステップ4: 定性判定

$$Qual\ Passed = (Qual\ Total \geq 15)$$

### 6.5 ステップ5: 最終判定

$$Final\ Decision = \begin{cases}
見送り & \text{if } (Quant\ Result = NG) \lor (Qual\ Total < 15) \\
見送りでない & \text{if } (Quant\ Result = OK) \land (Qual\ Total \geq 15)
\end{cases}$$

## 7. 例外処理と運用上の注意

### 7.1 数値未入力の扱い

- $Adj\ EBITDA$ 未入力により $ND/EBITDA$ が計算不能でも、ロジック上は「数値未入力」として定量NGに直結しない
- 実務上は「情報不足」として別途フラグ管理する設計余地がある

### 7.2 参考指標の扱い

- EV/Equity Valueはレンジ外でも「△」止まりであり、ゲートでは落ちない
- 投資サイズ適合の補助チェックという位置づけ

## 8. 計算例

### 8.1 入力データ例

- 売上高: 600百万円
- 調整後EBITDA: 120百万円
- Net Debt: 300百万円
- EBITDA倍率: 4.0倍
- 定性スコア: 適合度4点、ブランド4点、デジタル4点、希少性3点

### 8.2 計算プロセス

#### ステップ1: 中間計算

$$ND/EBITDA = \frac{300}{120} = 2.5$$

$$EV = 120 \times 4.0 = 480$$

$$Equity\ Value = 480 - 300 = 180$$

$$Qual\ Total = 4 + 4 + 4 + 3 = 15$$

#### ステップ2: 定量判定

- 売上高: 600 ≥ 500 → 〇
- 調整後EBITDA: 120 ≥ 100 → ◎
- ND/EBITDA: 2.5 ≤ 3 → ◎
- EBITDA倍率: 4.0 > 3 かつ 4.0 ≤ 4 → 〇
- EV: 480 < 1000 → △（参考）
- Equity Value: 180 < 300 → △（参考）

#### ステップ3: 定量総合判定

すべての判定が×ではないため：

$$Quant\ Result = OK$$

#### ステップ4: 定性判定

$$Qual\ Total = 15 \geq 15 \Rightarrow Qual\ Passed = True$$

#### ステップ5: 最終判定

$$(Quant\ Result = OK) \land (Qual\ Total = 15) \Rightarrow Final\ Decision = 見送りでない$$
