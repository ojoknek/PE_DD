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

$$ND/EBITDA = \frac{Net\ Debt}{Adj\ EBITDA}$$

ここで：
- $ND/EBITDA$: ND/EBITDA倍率（レバレッジ）
- $Net\ Debt$: 純有利子負債（有利子負債 - 現預金）
- $Adj\ EBITDA$: 調整後EBITDA

**計算条件**: $Adj\ EBITDA = 0$ または未入力の場合、$ND/EBITDA = null$（計算不能）

#### 1-2. EV（企業価値）

$$EV = Adj\ EBITDA \times EBITDA\ Multiple$$

ここで：
- $EV$: 企業価値（Enterprise Value）
- $Adj\ EBITDA$: 調整後EBITDA
- $EBITDA\ Multiple$: EBITDA倍率

**計算条件**: $Adj\ EBITDA$ または $EBITDA\ Multiple$ が未入力の場合、$EV = null$（計算不能）

#### 1-3. Equity Value（株主価値）

$$Equity\ Value = EV - Net\ Debt$$

ここで：
- $Equity\ Value$: 株主価値（Equity Value）
- $EV$: 企業価値（Enterprise Value）
- $Net\ Debt$: 純有利子負債（未入力の場合は0として扱う）

**計算条件**: $EV = null$ の場合、$Equity\ Value = null$（計算不能）

#### 1-4. 定性合計

$$Qual\ Total = Fit\ Score + Brand\ Score + Digital\ Score + Scarcity\ Score$$

ここで：
- $Qual\ Total$: 定性合計スコア（範囲: 4〜20点）
- $Fit\ Score$: 領域・業態適合度（1〜5点、未入力は0として扱う）
- $Brand\ Score$: ブランド・独自性（1〜5点、未入力は0として扱う）
- $Digital\ Score$: ファンベース・D2C（1〜5点、未入力は0として扱う）
- $Scarcity\ Score$: 特定分野・地域性（1〜5点、未入力は0として扱う）

---

### 2) 定量（財務）の離散判定（Discrete Ratings）

#### 2-1. 売上高判定

| 条件 | 判定 |
|------|------|
| $sales = null$ | 数値未入力 |
| $sales \geq 500$ | 〇 |
| $300 \leq sales < 500$ | △ |
| $sales < 300$ | × |

ここで：$sales$: 売上高（百万円単位）

#### 2-2. 調整後EBITDA判定

| 条件 | 判定 |
|------|------|
| $adj\_ebitda = null$ | 数値未入力 |
| $adj\_ebitda \geq 100$ | ◎ |
| $50 \leq adj\_ebitda < 100$ | 〇 |
| $adj\_ebitda < 50$ | × |

ここで：$adj\_ebitda$: 調整後EBITDA（百万円単位）

#### 2-3. ND/EBITDA判定

| 条件 | 判定 |
|------|------|
| $nd\_to\_ebitda = null$ | 数値未入力 |
| $nd\_to\_ebitda \leq 3$ | ◎ |
| $3 < nd\_to\_ebitda \leq 4$ | 〇 |
| $nd\_to\_ebitda > 4$ | × |

#### 2-4. EBITDA倍率判定

| 条件 | 判定 |
|------|------|
| $ebitda\_multiple = null$ | 数値未入力 |
| $ebitda\_multiple \leq 3$ | ◎ |
| $3 < ebitda\_multiple \leq 4$ | 〇 |
| $ebitda\_multiple > 4$ | × |

#### 2-5. EV判定（参考：サイズ適合）

| 条件 | 判定 |
|------|------|
| $ev = null$ | （空欄） |
| $1000 \leq ev \leq 2500$ | 〇 |
| 上記以外 | △ |

**注意**: EVは×判定を持たない（ゲート要因にしない）

#### 2-6. Equity Value判定（参考：サイズ適合）

| 条件 | 判定 |
|------|------|
| $equity\_value = null$ | 数値未入力 |
| $300 \leq equity\_value \leq 1500$ | 〇 |
| 上記以外 | △ |

**注意**: Equity Valueは×判定を持たない（ゲート要因にしない）

---

### 3) 定量総合判定（Quant Gate）

$$Quant\ Result = \begin{cases}
NG & \text{if } \exists rating \in \{sales, adj\_ebitda, nd\_to\_ebitda, ebitda\_multiple\} : rating = \times \\
OK & \text{otherwise}
\end{cases}$$

論理式で表現すると：

$$Quant\ Result = \begin{cases}
NG & \text{if } (sales\_rating = \times) \lor (adj\_ebitda\_rating = \times) \lor (nd\_to\_ebitda\_rating = \times) \lor (ebitda\_multiple\_rating = \times) \\
OK & \text{otherwise}
\end{cases}$$

### 4) 定性判定（Qual Gate）

$$Qual\ Passed = \begin{cases}
True & \text{if } Qual\ Total \geq 15 \\
False & \text{if } Qual\ Total < 15
\end{cases}$$

ここで：
- $Qual\ Passed$: 定性ゲート合格フラグ（True: 合格、False: 不合格）
- $Qual\ Total$: 定性合計スコア（4〜20点）
- 合格基準: 15点以上

### 5) 最終判定（見送り/見送りでない）

#### 見送り条件（Skip）

$$Skip = (Quant\ Result = NG) \lor (Qual\ Total < 15)$$

論理式で表現すると：

$$Skip = (Quant\ Result = NG) \lor \neg Qual\ Passed$$

#### 見送りでない条件（Pass）

$$Pass = (Quant\ Result = OK) \land (Qual\ Total \geq 15)$$

論理式で表現すると：

$$Pass = (Quant\ Result = OK) \land Qual\ Passed$$

#### 最終判定の決定

$$Final\ Decision = \begin{cases}
見送り & \text{if } Skip \\
見送りでない & \text{if } Pass
\end{cases}$$

---

### 6) 例外（運用上の注意）
- `adj_ebitda` 未入力により `nd_to_ebitda` が計算不能でも、ロジック上は「数値未入力」として定量NGに直結しない  
  → 実務上は「情報不足」として別途フラグ管理する設計余地がある
- EV/Equity Valueはレンジ外でも「△」止まりであり、ゲートでは落ちない（投資サイズ適合の補助チェックという位置づけ）

## 詳細な数式仕様

詳細な数式仕様については、以下のドキュメントを参照してください：

- [nn_dd_calculator.md](nn_dd_calculator.md) - NN DD計算ロジックの数式仕様書
- [financial_metrics.md](financial_metrics.md) - 財務指標計算の数式仕様書
- [valuation_metrics.md](valuation_metrics.md) - バリュエーション指標計算の数式仕様書

## 実装方法

### プロンプトベース実装

計算ロジックは、AI/LLMを使用したプロンプトベースで実装可能です。数式仕様書を参照して、適切な計算式を適用してください。

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

## ファイル構成

```
calculations/
├── nn_dd_calculator.md          # NN DD計算ロジックの数式仕様書
├── financial_metrics.md         # 財務指標計算の数式仕様書
├── valuation_metrics.md         # バリュエーション指標計算の数式仕様書
├── CHANGELOG.md                 # 改善履歴
└── README.md                    # このファイル
```

## 参考文献
- `dd_logic/references/web/壁の道の向こう側/` - 財務モデリングの実践的手法
  - DCF法による企業価値評価の基礎
  - 財務諸表の分析手法
  - バリュエーション分析の実務
- `dd_logic/EVALUATION_POINTS_README.md` - 評価論点管理システム
- `dd_logic/nn_dd/criteria/evaluation_criteria.md` - NN DD評価基準

## 補足説明

### EBITDAの定義
NN DDでは、調整後EBITDAを使用します。IM DDと同様に、以下の3つのCを満たす利益をカウントします：
- **Core**: その会社の本業からの収益であること
- **Continuing**: その事業が継続していること
- **Controlled**: その事業を支配していること

### Net Debtの計算
```
Net Debt = 有利子負債 - 現預金
```
- 有利子負債: 短期借入金、長期借入金、社債等
- 現預金: 現金及び預金、短期有価証券等

### バリュエーション指標の補足
- **EV（企業価値）**: 調整後EBITDA × EBITDA倍率
- **Equity Value（株主価値）**: EV - Net Debt
- これらの指標は投資サイズ適合の補助チェックとして使用され、ゲート要因ではありません

## 改善履歴

### 2026年1月27日 - 参考文献に基づく精緻化
- ✅ 参考文献の内容を反映した補足説明の追加
- ✅ EBITDAの定義（3つのC）の明確化
- ✅ Net Debt計算の詳細説明
- ✅ バリュエーション指標の補足説明

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
