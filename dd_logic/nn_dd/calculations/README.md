# NN DD計算ロジック

## 概要
NN DD評価に使用する計算ロジックです。定量情報と定性情報を統合した結論導出ロジックを含みます。

本モジュールは、README.mdの仕様に完全準拠して実装されており、事業承継ファンドのNN_DD評価を効率的かつ正確に実行できます。

**主な特徴:**
- ✅ README.mdの仕様に完全準拠
- ✅ 定量・定性の両面から包括的な評価
- ✅ 離散判定（◎/〇/△/×）による明確な評価基準
- ✅ ゲート判定による自動的な見送り/見送りでないの判定
- ✅ 包括的なテストコードと実践的使用例

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

### 基本的な使用方法

NN_DD評価は`nn_dd_calculator.py`の`NNDDCalculator`クラスを使用して実行します。

```python
from nn_dd_calculator import NNDDCalculator

# インスタンス化
calc = NNDDCalculator()

# 全計算を一括実行（推奨）
result = calc.calculate_all(
    sales=600,              # 売上高（百万円）
    adj_ebitda=120,         # 調整後EBITDA（百万円）
    net_debt=300,           # Net Debt（百万円）
    ebitda_multiple=4.0,    # EBITDA倍率
    fit_score=4,            # 領域・業態適合度（1〜5点）
    brand_score=4,          # ブランド・独自性（1〜5点）
    digital_score=4,        # ファンベース・D2C（1〜5点）
    scarcity_score=3        # 特定分野・地域性（1〜5点）
)

# 結果の確認
print(f"最終判定: {result['final_decision']}")
print(f"定量ゲート: {result['gate_results']['quantitative']}")
print(f"定性ゲート: {result['gate_results']['qualitative']}")

# NG理由の確認
if result['reasoning']['quantitative_ng_reasons']:
    for reason in result['reasoning']['quantitative_ng_reasons']:
        print(f"  - {reason}")
```

### 個別計算メソッド

必要に応じて、個別の計算メソッドも使用できます。

```python
# 中間計算
nd_to_ebitda = calc.calculate_nd_to_ebitda(net_debt=300, adj_ebitda=120)
ev = calc.calculate_ev(adj_ebitda=120, ebitda_multiple=4.0)
equity_value = calc.calculate_equity_value(ev=480, net_debt=300)
qual_total = calc.calculate_qualitative_total(4, 4, 4, 3)

# 定量判定
sales_rating = calc.rate_sales(600)  # Rating.GOOD
ebitda_rating = calc.rate_adj_ebitda(120)  # Rating.EXCELLENT

# ゲート判定
quant_result = calc.evaluate_quantitative_gate(
    sales_rating, ebitda_rating, nd_to_ebitda_rating, multiple_rating
)
qual_passed = calc.evaluate_qualitative_gate(qual_total)

# 最終判定
decision = calc.make_final_decision(quant_result, qual_passed)
```

### 実装ファイル

#### 1. `nn_dd_calculator.py` - メイン計算モジュール
README.mdの仕様に完全準拠した計算システム。

**主な機能:**
- 中間計算（ND/EBITDA、EV、Equity Value、定性合計）
- 定量判定の離散化（売上高、EBITDA、ND/EBITDA、倍率、EV、Equity Value）
- 定量総合判定（Quant Gate）
- 定性判定（Qual Gate）
- 最終判定（見送り/見送りでない）

**主要メソッド:**
- `calculate_all()` - 全計算を一括実行（推奨）
- `calculate_nd_to_ebitda()` - ND/EBITDA計算
- `calculate_ev()` - EV計算
- `calculate_equity_value()` - Equity Value計算
- `calculate_qualitative_total()` - 定性合計計算
- `rate_sales()`, `rate_adj_ebitda()` 等 - 各項目の判定
- `evaluate_quantitative_gate()` - 定量ゲート判定
- `evaluate_qualitative_gate()` - 定性ゲート判定
- `make_final_decision()` - 最終判定

#### 2. `financial_metrics.py` - 財務指標計算
包括的な財務指標の計算機能（補助機能）。

**主な機能:**
- `calculate_cagr()` - CAGR（売上成長率）
- `calculate_ebitda_margin()` - EBITDAマージン
- `calculate_operating_margin()` - 営業利益率
- `calculate_roe()` - ROE（自己資本利益率）
- `calculate_roa()` - ROA（総資産利益率）
- `calculate_debt_to_equity_ratio()` - 負債資本比率
- `calculate_current_ratio()` - 流動比率
- `calculate_quick_ratio()` - 当座比率
- `calculate_working_capital()` - 運転資金
- `calculate_working_capital_turnover()` - 運転資金回転率
- `calculate_comprehensive_financial_metrics()` - 上記の一括計算

**注意:** このファイルはREADME.mdの仕様には直接含まれていませんが、財務分析の補助機能として提供されています。

#### 3. `valuation_metrics.py` - バリュエーション指標計算
README.mdの仕様に基づく、NN_DD評価に必要なバリュエーション計算機能。

**主な機能（README.md仕様準拠）:**
- `calculate_net_debt()` - Net Debt計算（有利子負債−現預金）
- `calculate_enterprise_value_from_ebitda()` - EV計算（EBITDA倍率から）
- `calculate_equity_value_from_ev()` - Equity Value計算（EVから）

**注意:** このファイルはREADME.mdの仕様に完全準拠しており、仕様外のメソッドは削除されています。

## 出力形式
計算結果は構造化されたJSON形式で出力されます。

### `calculate_all()`の出力例

```json
{
  "derived_metrics": {
    "nd_to_ebitda": 2.5,
    "ev": 480.0,
    "equity_value": 180.0,
    "qualitative_total": 15
  },
  "quantitative_ratings": {
    "sales": "〇",
    "adj_ebitda": "◎",
    "nd_to_ebitda": "◎",
    "ebitda_multiple": "〇",
    "ev": "△",
    "equity_value": "△"
  },
  "gate_results": {
    "quantitative": "OK",
    "qualitative": "合格"
  },
  "final_decision": "見送りでない",
  "reasoning": {
    "quantitative_ng_reasons": [],
    "qualitative_score": 15,
    "qualitative_threshold": 15
  }
}
```

## テストと使用例

### テストコード
```bash
python3 test_nn_dd_calculator.py
```

### 使用例
```bash
python3 example_usage.py
```

実践的な使用例が5パターン含まれています：
1. **見送りでない案件（合格）** - 定量・定性ともに合格したケース
2. **見送り案件（定量NG）** - 売上高不足などで定量ゲートNG
3. **見送り案件（定性不合格）** - 定性スコアが15点未満
4. **包括的な財務分析との統合** - `financial_metrics.py`との連携例
5. **センシティビティ分析** - EBITDA倍率の変化による影響分析

### テスト結果

全テストが成功しています：
- ✅ 中間計算のテスト（正常系・異常系）
- ✅ 定量判定のテスト（全6項目）
- ✅ ゲート判定のテスト（OK/NGケース）
- ✅ 最終判定のテスト（4パターン）
- ✅ 統合計算のテスト（3ケース）

## ファイル構成

```
calculations/
├── nn_dd_calculator.py          # メイン計算モジュール（README.md仕様完全準拠）
├── valuation_metrics.py        # バリュエーション計算（README.md仕様準拠）
├── financial_metrics.py         # 財務指標計算（補助機能）
├── test_nn_dd_calculator.py     # テストコード
├── example_usage.py             # 実践的使用例
├── CHANGELOG.md                  # 改善履歴
└── README.md                     # このファイル
```

## 改善履歴

### 2026年1月22日 - 最終整理
- ✅ README.mdの仕様に完全準拠した実装
- ✅ 不要な計算メソッドの削除（`scoring.py`削除、`valuation_metrics.py`整理）
- ✅ 定量論点と定性論点の明確な分離
- ✅ 離散判定（◎/〇/△/×）の実装
- ✅ ゲート判定ロジックの実装
- ✅ 包括的なテストコードの追加（5カテゴリ、全ケース成功）
- ✅ 実践的な使用例の追加（5パターン）
- ✅ 既存ファイル（financial_metrics.py, valuation_metrics.py）の拡張

### 削除されたファイル
- `scoring.py` - README.mdの仕様に含まれていないため削除

### 整理されたファイル
- `valuation_metrics.py` - README.mdの仕様に必要なメソッドのみ保持
  - 削除: EV/Sales倍率、EV/EBITDA倍率、PBR、PER等の仕様外メソッド
