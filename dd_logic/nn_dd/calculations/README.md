# NN DD計算ロジック

## 概要
NN DD評価に使用する計算ロジックです。定量情報と定性情報を統合した結論導出ロジックを含みます。

## 計算項目

### 1) 中間計算（Derived Metrics）
#### 1-1. ND/EBITDA（レバレッジ）
- 定義：`nd_to_ebitda = net_debt / adj_ebitda`
- 条件：`adj_ebitda` が0または未入力の場合、`nd_to_ebitda = null`

#### 1-2. EV（企業価値）
- 定義：`ev = adj_ebitda * ebitda_multiple`
- 条件：`adj_ebitda` または `ebitda_multiple` が未入力の場合、`ev = null`

#### 1-3. Equity Value（株主価値）
- 定義：`equity_value = ev - net_debt`
- 条件：`ev` がnullの場合、`equity_value = null`

#### 1-4. 定性合計
- 定義：`qual_total = fit_score + brand_score + digital_score + scarcity_score`
- 範囲：4..20

---

### 2) 定量（財務）の離散判定（Discrete Ratings）
#### 2-1. 売上高判定
- `sales >= 500` → `〇`
- `300 <= sales < 500` → `△`
- `sales < 300` → `×`

#### 2-2. 調整後EBITDA判定
- `adj_ebitda >= 100` → `◎`
- `50 <= adj_ebitda < 100` → `〇`
- `adj_ebitda < 50` → `×`

#### 2-3. ND/EBITDA判定
- `nd_to_ebitda` がnull → `数値未入力`
- `nd_to_ebitda <= 3` → `◎`
- `3 < nd_to_ebitda <= 4` → `〇`
- `nd_to_ebitda > 4` → `×`

#### 2-4. EBITDA倍率判定
- `ebitda_multiple` が未入力 → `数値未入力`
- `ebitda_multiple <= 3` → `◎`
- `3 < ebitda_multiple <= 4` → `〇`
- `ebitda_multiple > 4` → `×`

#### 2-5. EV判定（参考：サイズ適合）
- `ev` がnull → `（空欄）`
- `1000 <= ev <= 2500` → `〇`
- 上記以外 → `△`
- 注：EVは×判定を持たない（ゲート要因にしない）

#### 2-6. Equity Value判定（参考：サイズ適合）
- `equity_value` がnull → `数値未入力`
- `300 <= equity_value <= 1500` → `〇`
- 上記以外 → `△`
- 注：Equity Valueは×判定を持たない（ゲート要因にしない）

---

### 3) 定量総合判定（Quant Gate）
- 定義：定量判定の対象範囲に **×が1つでもある** 場合 `NG`、なければ `OK`
- 擬似式：
  - `quant_result = (exists "×") ? NG : OK`

---

### 4) 定性判定（Qual Gate）
- 定義：
  - `qual_total >= 15` → 合格
  - `qual_total < 15` → 不合格

---

### 5) 最終判定（見送り/見送りでない）
#### 見送り条件（Skip）
- `skip = (quant_result == NG) OR (qual_total < 15)`

#### 見送りでない条件（Pass）
- `pass = (quant_result == OK) AND (qual_total >= 15)`

---

### 6) 例外（運用上の注意）
- `adj_ebitda` 未入力により `nd_to_ebitda` が計算不能でも、ロジック上は「数値未入力」として定量NGに直結しない  
  → 実務上は「情報不足」として別途フラグ管理する設計余地がある
- EV/Equity Valueはレンジ外でも「△」止まりであり、ゲートでは落ちない（投資サイズ適合の補助チェックという位置づけ）

## 実装方法
各計算ロジックは、Pythonスクリプトまたはプロンプトベースで実装可能です。

## 出力形式
計算結果は構造化されたJSON形式で出力されます。
