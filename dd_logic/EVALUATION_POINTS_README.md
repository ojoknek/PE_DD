# 事業承継ファンド向け評価論点管理システム

## 概要

`evaluation_points_manager.py`は、PEファンドの事業承継投資における定量論点・定性論点を体系的に管理するPythonモジュールです。

## 主な特徴

### 1. 定量論点と定性論点の明確な分離

- **定量論点（Quantitative Points）**: 財務数値や指標に基づく客観的な評価項目
- **定性論点（Qualitative Points）**: 経営陣、組織、事業環境など質的な評価項目

### 2. 事業承継投資に特化した評価項目

#### NN_DDフェーズ（ノンネームDD）

**定量論点（ウェイト合計: 55%）**
- 財務パフォーマンス（20%）★クリティカル
- 財務健全性（15%）★クリティカル
- 市場規模（10%）
- 予備的バリュエーション（10%）★クリティカル

**定性論点（ウェイト合計: 45%）**
- 事業承継の背景（15%）★クリティカル
- ビジネスモデル（10%）★クリティカル
- 経営・組織（10%）★クリティカル
- 取引関係（5%）
- 投資適合性（5%）

#### IM_DDフェーズ（IM精査DD）

**定量論点（ウェイト合計: 55%）**
- 詳細財務分析（20%）★クリティカル
- 運転資金・キャッシュフロー（15%）★クリティカル
- バリュエーション分析（15%）★クリティカル
- KPI分析（5%）

**定性論点（ウェイト合計: 45%）**
- 承継実行計画（12%）★クリティカル
- 事業持続可能性（10%）★クリティカル
- 組織能力（8%）★クリティカル
- ステークホルダー関係（7%）★クリティカル
- リスク・コンプライアンス（5%）★クリティカル
- バリュークリエーション計画（3%）

### 3. 豊富な機能

- クリティカル論点の自動抽出
- カテゴリ別スコア計算（加重平均）
- チェックリスト自動生成
- 事業承継特有論点の抽出
- Markdown形式でのエクスポート

## 使用方法

### 基本的な使い方

```python
from evaluation_points_manager import EvaluationPointsManager

# インスタンス化
manager = EvaluationPointsManager()

# NN_DDの評価フレームワークを表示
manager.print_evaluation_framework('nn_dd')

# IM_DDの評価フレームワークを表示
manager.print_evaluation_framework('im_dd')
```

### 定量論点・定性論点の取得

```python
# 定量論点のみ取得
quantitative = manager.get_quantitative_points('nn_dd')

# 定性論点のみ取得
qualitative = manager.get_qualitative_points('nn_dd')

# 両方取得
all_points = manager.get_evaluation_points('nn_dd')
```

### クリティカル論点の取得

```python
# クリティカルな論点のみ抽出
critical = manager.get_critical_points('nn_dd')

print(f"定量クリティカル: {list(critical['quantitative'].keys())}")
print(f"定性クリティカル: {list(critical['qualitative'].keys())}")
```

### 事業承継特有論点の取得

```python
# 事業承継に関連する重要論点を抽出
succession = manager.get_succession_specific_points('nn_dd')

for point_name, point_data in succession.items():
    print(f"\n{point_name}:")
    for sub in point_data['sub_points']:
        print(f"  - {sub}")
```

### スコア計算

```python
# 各論点のスコアを設定（0〜100点）
scores = {
    'financial_performance': 85.0,
    'financial_health': 90.0,
    'market_size': 75.0,
    'preliminary_valuation': 80.0
}

# カテゴリ全体の加重平均スコアを計算
avg_score, details = manager.calculate_category_score(
    'nn_dd', 
    'quantitative', 
    scores
)

print(f"定量論点の総合スコア: {avg_score:.1f}点")

# 各論点の詳細を確認
for point_name, detail in details.items():
    print(f"{point_name}: {detail['score']}点 (ウェイト: {detail['weight']:.1%})")
```

### チェックリスト生成

```python
# 全論点のチェックリストを生成
checklist = manager.generate_checklist('nn_dd')

for item in checklist:
    critical = "★" if item['critical'] else " "
    print(f"{critical} [{item['category']}] {item['sub_point']}")
    print(f"   データソース: {', '.join(item['data_sources'])}")

# 定量論点のみのチェックリスト
quant_checklist = manager.generate_checklist('nn_dd', 'quantitative')
```

### Markdown形式でエクスポート

```python
from pathlib import Path

# NN_DDフレームワークをMarkdownファイルとして出力
output_path = Path('./nn_dd_framework.md')
manager.export_to_markdown('nn_dd', output_path)

# IM_DDフレームワークをMarkdownファイルとして出力
output_path = Path('./im_dd_framework.md')
manager.export_to_markdown('im_dd', output_path)
```

### カスタム設定の保存・読み込み

```python
# デフォルト設定を修正
manager.update_point_weight('nn_dd', 'quantitative', 'financial_performance', 0.25)

# 設定をJSONファイルに保存
config_path = Path('./custom_config.json')
manager.save_config(config_path)

# カスタム設定を読み込んで新しいインスタンスを作成
custom_manager = EvaluationPointsManager(config_path)
```

## 実践的な使用例

### ケース1: NN_DD段階でのスクリーニング

```python
manager = EvaluationPointsManager()

# クリティカル論点のみに絞って評価
critical = manager.get_critical_points('nn_dd')

# 定量クリティカル論点の評価
quant_scores = {
    'financial_performance': 80,  # 過去実績は良好
    'financial_health': 65,       # 負債がやや多い
    'preliminary_valuation': 70   # バリュエーションは許容範囲
}

quant_score, _ = manager.calculate_category_score(
    'nn_dd', 'quantitative', quant_scores
)

# 定性クリティカル論点の評価
qual_scores = {
    'succession_background': 85,  # 後継者不在で明確な承継ニーズ
    'business_model': 75,         # ビジネスモデルは堅実
    'management_organization': 60 # 経営陣の高齢化が課題
}

qual_score, _ = manager.calculate_category_score(
    'nn_dd', 'qualitative', qual_scores
)

# 総合判断
overall = (quant_score * 0.6 + qual_score * 0.4)  # 定量60%, 定性40%
print(f"NN_DD総合スコア: {overall:.1f}点")

if overall >= 70 and quant_score >= 65:
    print("判定: IM取得を推奨")
else:
    print("判定: 見送り")
```

### ケース2: IM_DD段階での詳細評価

```python
manager = EvaluationPointsManager()

# チェックリストを使って漏れなく評価
checklist = manager.generate_checklist('im_dd')

# 各項目を評価してスコアを記録
evaluation_results = {}
for item in checklist:
    # 実際の評価作業で各項目をチェック
    # ここではサンプルとして仮のスコアを設定
    pass

# 事業承継特有論点を重点的に確認
succession = manager.get_succession_specific_points('im_dd')
print("\n【事業承継の実行可能性評価】")
for point_name, point_data in succession.items():
    print(f"\n{point_name}:")
    for sub in point_data['sub_points']:
        print(f"  □ {sub}")

# データソースの確認
print("\n【必要なデータソース】")
for point_name, point_data in succession.items():
    sources = point_data.get('data_sources', [])
    print(f"{point_name}: {', '.join(sources)}")
```

## データ構造

各論点は以下の情報を持ちます：

```python
{
    'category': 'quantitative' or 'qualitative',  # カテゴリ
    'weight': 0.20,                                # ウェイト（0.0〜1.0）
    'sub_points': [                                # サブ論点のリスト
        'サブ論点1',
        'サブ論点2',
        ...
    ],
    'data_sources': [                              # データソースのリスト
        'ノンネーム資料',
        '財務諸表',
        ...
    ],
    'critical': True or False                      # クリティカルフラグ
}
```

## カスタマイズ

評価項目や重みはファンドの投資方針に応じてカスタマイズできます：

1. `_default_config()`メソッドを直接編集
2. JSON設定ファイルを作成して読み込み
3. `update_point_weight()`メソッドで個別に更新

## 関連ファイル

- `dd_logic/nn_dd/criteria/evaluation_criteria.md` - ノンネームDD評価基準
- `dd_logic/im_dd/evaluation_points/evaluation_points.md` - IM_DD評価論点
- `dd_logic/references/` - 財務モデリング参考資料

## ライセンス

このモジュールは事業承継ファンドのDD業務を支援するために作成されています。
