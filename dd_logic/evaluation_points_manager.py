"""
事業承継ファンド向け論点管理システム

PEファンドによる事業承継投資における定量論点・定性論点を管理します。
- 定量論点: 財務数値や指標に基づく客観的な評価項目
- 定性論点: 経営陣、組織、事業環境など質的な評価項目
"""
from typing import Dict, List, Optional, Tuple
import json
from pathlib import Path
from enum import Enum


class PointCategory(Enum):
    """論点カテゴリ"""
    QUANTITATIVE = "quantitative"  # 定量論点
    QUALITATIVE = "qualitative"    # 定性論点


class WorkflowType(Enum):
    """ワークフロータイプ"""
    NN_DD = "nn_dd"  # ノンネームDD
    IM_DD = "im_dd"  # IM精査DD


class EvaluationPointsManager:
    """
    事業承継ファンド向け評価論点管理クラス
    
    定量論点と定性論点を体系的に管理し、
    事業承継投資における意思決定をサポートします。
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        初期化
        
        Args:
            config_path: 設定ファイルのパス（Noneの場合はデフォルト設定を使用）
        """
        self.config_path = config_path
        self.evaluation_points = {}
        self.load_config()
    
    def load_config(self):
        """
        設定ファイルを読み込む
        """
        if self.config_path and self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.evaluation_points = json.load(f)
        else:
            self.evaluation_points = self._default_config()
    
    def _default_config(self) -> Dict:
        """
        事業承継ファンド向けデフォルト設定
        
        定量論点と定性論点を明確に分けた評価フレームワーク
        """
        return {
            'nn_dd': {
                # ========== 定量論点（Quantitative Points） ==========
                'quantitative': {
                    'financial_performance': {
                        'category': 'quantitative',
                        'weight': 0.20,
                        'sub_points': [
                            '過去3〜5年の売上高推移',
                            '営業利益・EBITDAの推移',
                            '売上高営業利益率',
                            '売上高成長率（CAGR）',
                            'ROE・ROAの推移'
                        ],
                        'data_sources': ['ノンネーム資料', '財務サマリー'],
                        'critical': True
                    },
                    'financial_health': {
                        'category': 'quantitative',
                        'weight': 0.15,
                        'sub_points': [
                            '自己資本比率',
                            '有利子負債残高',
                            'Debt/EBITDA倍率',
                            '流動比率・当座比率',
                            '運転資金の状況'
                        ],
                        'data_sources': ['ノンネーム資料', '財務サマリー'],
                        'critical': True
                    },
                    'market_size': {
                        'category': 'quantitative',
                        'weight': 0.10,
                        'sub_points': [
                            '対象市場規模（TAM）',
                            '市場成長率',
                            '市場シェア（推定）',
                            '顧客数・取引社数'
                        ],
                        'data_sources': ['ノンネーム資料', '市場調査レポート'],
                        'critical': False
                    },
                    'preliminary_valuation': {
                        'category': 'quantitative',
                        'weight': 0.10,
                        'sub_points': [
                            '希望売却価格（提示価格）',
                            'EV/EBITDA倍率（想定）',
                            '類似上場企業倍率との比較',
                            '投資回収期間（想定）'
                        ],
                        'data_sources': ['ノンネーム資料', 'ティーザー'],
                        'critical': True
                    }
                },
                # ========== 定性論点（Qualitative Points） ==========
                'qualitative': {
                    'succession_background': {
                        'category': 'qualitative',
                        'weight': 0.15,
                        'sub_points': [
                            '事業承継の背景・理由',
                            '後継者不在の状況',
                            '創業者・現オーナーの年齢・健康状態',
                            '承継に向けた準備状況',
                            'オーナーの承継後の関与意向'
                        ],
                        'data_sources': ['ノンネーム資料', 'ティーザー'],
                        'critical': True
                    },
                    'business_model': {
                        'category': 'qualitative',
                        'weight': 0.10,
                        'sub_points': [
                            '事業内容の理解容易性',
                            'ビジネスモデルの持続可能性',
                            '収益構造の安定性',
                            '競合優位性（差別化要因）',
                            '参入障壁の有無'
                        ],
                        'data_sources': ['ノンネーム資料', 'ティーザー'],
                        'critical': True
                    },
                    'management_organization': {
                        'category': 'qualitative',
                        'weight': 0.10,
                        'sub_points': [
                            '経営陣の構成・年齢',
                            'キーマンの有無と依存度',
                            '組織体制の整備状況',
                            '従業員数と平均年齢',
                            '離職率の状況'
                        ],
                        'data_sources': ['ノンネーム資料'],
                        'critical': True
                    },
                    'business_relationships': {
                        'category': 'qualitative',
                        'weight': 0.05,
                        'sub_points': [
                            '主要取引先の状況（集中度）',
                            '顧客基盤の安定性',
                            '仕入先との関係',
                            '地域性・商圏の特性',
                            'ブランド力・知名度'
                        ],
                        'data_sources': ['ノンネーム資料'],
                        'critical': False
                    },
                    'investment_fit': {
                        'category': 'qualitative',
                        'weight': 0.05,
                        'sub_points': [
                            'ファンド戦略との整合性',
                            '投資テーマとの適合度',
                            'ポートフォリオとの相性',
                            'バリューアップ施策の検討余地',
                            '出口戦略の実現可能性（想定）'
                        ],
                        'data_sources': ['内部検討'],
                        'critical': False
                    }
                }
            },
            'im_dd': {
                # ========== 定量論点（Quantitative Points） ==========
                'quantitative': {
                    'detailed_financial_analysis': {
                        'category': 'quantitative',
                        'weight': 0.20,
                        'sub_points': [
                            '過去5期の詳細財務分析',
                            '月次推移の分析',
                            'セグメント別収益性',
                            '非経常項目の調整',
                            '正常収益力（Normalized EBITDA）',
                            'Net Debt算定'
                        ],
                        'data_sources': ['IM', '財務諸表', '試算表'],
                        'critical': True
                    },
                    'working_capital_cashflow': {
                        'category': 'quantitative',
                        'weight': 0.15,
                        'sub_points': [
                            '運転資金の詳細分析',
                            '売掛金・在庫・買掛金回転期間',
                            'FCFの算定と推移',
                            '設備投資の実態',
                            '資金繰りの安定性'
                        ],
                        'data_sources': ['IM', '財務諸表', '管理資料'],
                        'critical': True
                    },
                    'valuation_analysis': {
                        'category': 'quantitative',
                        'weight': 0.15,
                        'sub_points': [
                            'DCF法による企業価値評価',
                            'マルチプル法（EV/EBITDA等）',
                            '類似取引比較',
                            '事業計画の妥当性検証',
                            'IRR・MOICシミュレーション',
                            'センシティビティ分析'
                        ],
                        'data_sources': ['IM', '事業計画', '市場データ'],
                        'critical': True
                    },
                    'kpi_analysis': {
                        'category': 'quantitative',
                        'weight': 0.05,
                        'sub_points': [
                            '事業KPIの推移分析',
                            '顧客単価・リピート率',
                            '生産性指標',
                            'マーケティングROI',
                            '各種効率性指標'
                        ],
                        'data_sources': ['IM', '管理資料'],
                        'critical': False
                    }
                },
                # ========== 定性論点（Qualitative Points） ==========
                'qualitative': {
                    'succession_execution': {
                        'category': 'qualitative',
                        'weight': 0.12,
                        'sub_points': [
                            '承継スキームの詳細',
                            '創業者の引退計画',
                            '現経営陣の継続意向',
                            '後継経営者の選定・育成計画',
                            'キーマンの引き留め策',
                            '従業員への説明・コミュニケーション計画'
                        ],
                        'data_sources': ['IM', 'Q&A', 'マネジメントミーティング'],
                        'critical': True
                    },
                    'business_sustainability': {
                        'category': 'qualitative',
                        'weight': 0.10,
                        'sub_points': [
                            '競合環境の詳細分析',
                            '技術革新・デジタル化対応',
                            '参入障壁の堅牢性',
                            'ビジネスモデルの陳腐化リスク',
                            'サプライチェーンの安定性',
                            '規制・法規制の変更リスク'
                        ],
                        'data_sources': ['IM', '市場調査', '専門家ヒアリング'],
                        'critical': True
                    },
                    'organizational_capability': {
                        'category': 'qualitative',
                        'weight': 0.08,
                        'sub_points': [
                            '経営陣の能力・実績評価',
                            '組織ガバナンス体制',
                            '人材育成・採用体制',
                            '業務プロセスの標準化',
                            'IT・システム整備状況',
                            '企業文化・価値観の評価'
                        ],
                        'data_sources': ['IM', 'マネジメントミーティング', '現地視察'],
                        'critical': True
                    },
                    'stakeholder_relationships': {
                        'category': 'qualitative',
                        'weight': 0.07,
                        'sub_points': [
                            '主要顧客との契約・関係性',
                            '仕入先との取引条件',
                            '金融機関との関係',
                            '地域社会・自治体との関係',
                            '労働組合の有無と関係性',
                            '知的財産権の保護状況'
                        ],
                        'data_sources': ['IM', 'Q&A', '契約書レビュー'],
                        'critical': True
                    },
                    'risk_compliance': {
                        'category': 'qualitative',
                        'weight': 0.05,
                        'sub_points': [
                            '法的リスクの有無',
                            'コンプライアンス体制',
                            '訴訟・係争案件',
                            '環境・安全衛生リスク',
                            '情報セキュリティ対策',
                            '事業継続計画（BCP）'
                        ],
                        'data_sources': ['IM', '法務DD', 'コンプライアンスチェック'],
                        'critical': True
                    },
                    'value_creation_plan': {
                        'category': 'qualitative',
                        'weight': 0.03,
                        'sub_points': [
                            'バリューアップ施策の具体性',
                            '追加投資の必要性',
                            'M&Aによる拡大可能性',
                            'デジタル化・DX推進余地',
                            '出口戦略の実現性',
                            'ESG対応の必要性'
                        ],
                        'data_sources': ['内部検討', '外部アドバイザー'],
                        'critical': False
                    }
                }
            }
        }
    
    def get_evaluation_points(self, workflow_type: str, category: Optional[str] = None) -> Dict:
        """
        評価論点を取得
        
        Args:
            workflow_type: ワークフロータイプ（'nn_dd' または 'im_dd'）
            category: 論点カテゴリ（'quantitative' または 'qualitative'、Noneの場合は両方）
        
        Returns:
            評価論点の辞書
        """
        workflow_points = self.evaluation_points.get(workflow_type, {})
        
        if category:
            return workflow_points.get(category, {})
        
        return workflow_points
    
    def get_quantitative_points(self, workflow_type: str) -> Dict:
        """
        定量論点のみを取得
        
        Args:
            workflow_type: ワークフロータイプ
        
        Returns:
            定量論点の辞書
        """
        return self.get_evaluation_points(workflow_type, 'quantitative')
    
    def get_qualitative_points(self, workflow_type: str) -> Dict:
        """
        定性論点のみを取得
        
        Args:
            workflow_type: ワークフロータイプ
        
        Returns:
            定性論点の辞書
        """
        return self.get_evaluation_points(workflow_type, 'qualitative')
    
    def get_point_weight(self, workflow_type: str, category: str, point_name: str) -> float:
        """
        論点の重みを取得
        
        Args:
            workflow_type: ワークフロータイプ
            category: カテゴリ（'quantitative' または 'qualitative'）
            point_name: 論点名
        
        Returns:
            重み（0.0〜1.0）
        """
        points = self.get_evaluation_points(workflow_type, category)
        if point_name in points:
            return points[point_name].get('weight', 0.0)
        return 0.0
    
    def get_critical_points(self, workflow_type: str, category: Optional[str] = None) -> Dict:
        """
        クリティカルな論点のみを取得
        
        Args:
            workflow_type: ワークフロータイプ
            category: カテゴリ（Noneの場合は両方）
        
        Returns:
            クリティカルな論点の辞書
        """
        all_points = self.get_evaluation_points(workflow_type, category)
        critical_points = {}
        
        if category:
            # 単一カテゴリの場合
            for point_name, point_data in all_points.items():
                if point_data.get('critical', False):
                    critical_points[point_name] = point_data
        else:
            # 両方のカテゴリを処理
            for cat in ['quantitative', 'qualitative']:
                cat_points = self.get_evaluation_points(workflow_type, cat)
                cat_critical = {}
                for point_name, point_data in cat_points.items():
                    if point_data.get('critical', False):
                        cat_critical[point_name] = point_data
                if cat_critical:
                    critical_points[cat] = cat_critical
        
        return critical_points
    
    def get_sub_points(self, workflow_type: str, category: str, point_name: str) -> List[str]:
        """
        サブ論点を取得
        
        Args:
            workflow_type: ワークフロータイプ
            category: カテゴリ（'quantitative' または 'qualitative'）
            point_name: 論点名
        
        Returns:
            サブ論点のリスト
        """
        points = self.get_evaluation_points(workflow_type, category)
        if point_name in points:
            return points[point_name].get('sub_points', [])
        return []
    
    def get_data_sources(self, workflow_type: str, category: str, point_name: str) -> List[str]:
        """
        データソースを取得
        
        Args:
            workflow_type: ワークフロータイプ
            category: カテゴリ
            point_name: 論点名
        
        Returns:
            データソースのリスト
        """
        points = self.get_evaluation_points(workflow_type, category)
        if point_name in points:
            return points[point_name].get('data_sources', [])
        return []
    
    def get_succession_specific_points(self, workflow_type: str) -> Dict:
        """
        事業承継特有の論点を取得
        
        事業承継に関連する重要論点をまとめて取得します。
        
        Args:
            workflow_type: ワークフロータイプ
        
        Returns:
            事業承継関連論点の辞書
        """
        succession_points = {}
        
        # 定性論点から事業承継関連を抽出
        qualitative = self.get_qualitative_points(workflow_type)
        
        if workflow_type == 'nn_dd':
            if 'succession_background' in qualitative:
                succession_points['succession_background'] = qualitative['succession_background']
            if 'management_organization' in qualitative:
                succession_points['management_organization'] = qualitative['management_organization']
        
        elif workflow_type == 'im_dd':
            if 'succession_execution' in qualitative:
                succession_points['succession_execution'] = qualitative['succession_execution']
            if 'organizational_capability' in qualitative:
                succession_points['organizational_capability'] = qualitative['organizational_capability']
        
        return succession_points
    
    def calculate_category_score(self, workflow_type: str, category: str, 
                                 point_scores: Dict[str, float]) -> Tuple[float, Dict]:
        """
        カテゴリ全体のスコアを計算
        
        Args:
            workflow_type: ワークフロータイプ
            category: カテゴリ（'quantitative' または 'qualitative'）
            point_scores: 各論点のスコア（0〜100）
        
        Returns:
            (加重平均スコア, 詳細情報)のタプル
        """
        points = self.get_evaluation_points(workflow_type, category)
        
        total_weight = 0.0
        weighted_sum = 0.0
        details = {}
        
        for point_name, point_data in points.items():
            if point_name in point_scores:
                weight = point_data.get('weight', 0.0)
                score = point_scores[point_name]
                weighted_sum += weight * score
                total_weight += weight
                
                details[point_name] = {
                    'score': score,
                    'weight': weight,
                    'weighted_score': weight * score,
                    'critical': point_data.get('critical', False)
                }
        
        average_score = weighted_sum / total_weight if total_weight > 0 else 0.0
        
        return average_score, details
    
    def generate_checklist(self, workflow_type: str, category: Optional[str] = None) -> List[Dict]:
        """
        チェックリストを生成
        
        Args:
            workflow_type: ワークフロータイプ
            category: カテゴリ（Noneの場合は両方）
        
        Returns:
            チェックリスト（各項目の詳細情報）
        """
        checklist = []
        
        categories = [category] if category else ['quantitative', 'qualitative']
        
        for cat in categories:
            points = self.get_evaluation_points(workflow_type, cat)
            
            for point_name, point_data in points.items():
                for sub_point in point_data.get('sub_points', []):
                    checklist.append({
                        'category': cat,
                        'point_name': point_name,
                        'sub_point': sub_point,
                        'weight': point_data.get('weight', 0.0),
                        'critical': point_data.get('critical', False),
                        'data_sources': point_data.get('data_sources', [])
                    })
        
        return checklist
    
    def save_config(self, output_path: Optional[Path] = None):
        """
        設定を保存
        
        Args:
            output_path: 出力パス（Noneの場合はconfig_pathを使用）
        """
        path = output_path or self.config_path
        if path:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(self.evaluation_points, f, ensure_ascii=False, indent=2)
    
    def update_point_weight(self, workflow_type: str, category: str, 
                           point_name: str, weight: float):
        """
        論点の重みを更新
        
        Args:
            workflow_type: ワークフロータイプ
            category: カテゴリ（'quantitative' または 'qualitative'）
            point_name: 論点名
            weight: 新しい重み（0.0〜1.0）
        """
        if workflow_type not in self.evaluation_points:
            self.evaluation_points[workflow_type] = {}
        
        if category not in self.evaluation_points[workflow_type]:
            self.evaluation_points[workflow_type][category] = {}
        
        if point_name not in self.evaluation_points[workflow_type][category]:
            self.evaluation_points[workflow_type][category][point_name] = {}
        
        self.evaluation_points[workflow_type][category][point_name]['weight'] = weight
    
    def print_evaluation_framework(self, workflow_type: str):
        """
        評価フレームワークを見やすく出力
        
        Args:
            workflow_type: ワークフロータイプ
        """
        print(f"\n{'='*80}")
        print(f"事業承継ファンド評価フレームワーク - {workflow_type.upper()}")
        print(f"{'='*80}\n")
        
        for category in ['quantitative', 'qualitative']:
            category_name = "定量論点" if category == 'quantitative' else "定性論点"
            print(f"\n【{category_name}】")
            print("-" * 80)
            
            points = self.get_evaluation_points(workflow_type, category)
            
            for point_name, point_data in points.items():
                critical_mark = " ★クリティカル" if point_data.get('critical', False) else ""
                weight = point_data.get('weight', 0.0)
                
                print(f"\n■ {point_name} (ウェイト: {weight:.1%}){critical_mark}")
                
                # サブ論点
                sub_points = point_data.get('sub_points', [])
                for i, sub in enumerate(sub_points, 1):
                    print(f"  {i}. {sub}")
                
                # データソース
                data_sources = point_data.get('data_sources', [])
                if data_sources:
                    print(f"  📊 データソース: {', '.join(data_sources)}")
        
        print(f"\n{'='*80}\n")
    
    def export_to_markdown(self, workflow_type: str, output_path: Path):
        """
        評価フレームワークをMarkdown形式でエクスポート
        
        Args:
            workflow_type: ワークフロータイプ
            output_path: 出力ファイルパス
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# 事業承継ファンド評価フレームワーク - {workflow_type.upper()}\n\n")
            
            for category in ['quantitative', 'qualitative']:
                category_name = "定量論点" if category == 'quantitative' else "定性論点"
                f.write(f"## {category_name}\n\n")
                
                points = self.get_evaluation_points(workflow_type, category)
                
                for point_name, point_data in points.items():
                    critical_mark = " ⭐" if point_data.get('critical', False) else ""
                    weight = point_data.get('weight', 0.0)
                    
                    f.write(f"### {point_name} (ウェイト: {weight:.1%}){critical_mark}\n\n")
                    
                    # サブ論点
                    sub_points = point_data.get('sub_points', [])
                    for sub in sub_points:
                        f.write(f"- {sub}\n")
                    
                    # データソース
                    data_sources = point_data.get('data_sources', [])
                    if data_sources:
                        f.write(f"\n**データソース**: {', '.join(data_sources)}\n")
                    
                    f.write("\n")
        
        print(f"✅ Markdownファイルを出力しました: {output_path}")


# ========== 使用例 ==========
if __name__ == "__main__":
    # マネージャーのインスタンス化
    manager = EvaluationPointsManager()
    
    # NN_DDフェーズの評価フレームワークを表示
    print("\n" + "="*80)
    print("使用例1: NN_DDフェーズの評価フレームワーク表示")
    print("="*80)
    manager.print_evaluation_framework('nn_dd')
    
    # 定量論点のみ取得
    print("\n" + "="*80)
    print("使用例2: NN_DDの定量論点のみ取得")
    print("="*80)
    quantitative = manager.get_quantitative_points('nn_dd')
    for point_name in quantitative.keys():
        print(f"- {point_name}")
    
    # クリティカルな論点のみ取得
    print("\n" + "="*80)
    print("使用例3: NN_DDのクリティカル論点取得")
    print("="*80)
    critical = manager.get_critical_points('nn_dd')
    print(f"定量: {list(critical.get('quantitative', {}).keys())}")
    print(f"定性: {list(critical.get('qualitative', {}).keys())}")
    
    # 事業承継特有論点の取得
    print("\n" + "="*80)
    print("使用例4: 事業承継特有論点の取得")
    print("="*80)
    succession = manager.get_succession_specific_points('nn_dd')
    for point_name, point_data in succession.items():
        print(f"\n■ {point_name}")
        for sub in point_data.get('sub_points', []):
            print(f"  - {sub}")
    
    # スコア計算の例
    print("\n" + "="*80)
    print("使用例5: カテゴリスコアの計算")
    print("="*80)
    sample_scores = {
        'financial_performance': 85.0,
        'financial_health': 90.0,
        'market_size': 75.0,
        'preliminary_valuation': 80.0
    }
    avg_score, details = manager.calculate_category_score('nn_dd', 'quantitative', sample_scores)
    print(f"定量論点の加重平均スコア: {avg_score:.1f}点")
    print("\n詳細:")
    for point_name, detail in details.items():
        print(f"  {point_name}: {detail['score']:.1f}点 (ウェイト: {detail['weight']:.1%})")
    
    # チェックリスト生成
    print("\n" + "="*80)
    print("使用例6: チェックリスト生成（定量論点のみ、最初の5項目）")
    print("="*80)
    checklist = manager.generate_checklist('nn_dd', 'quantitative')
    for i, item in enumerate(checklist[:5], 1):
        critical = "★" if item['critical'] else " "
        print(f"{critical} {i}. [{item['point_name']}] {item['sub_point']}")
    
    print(f"\n... 他 {len(checklist) - 5}項目\n")
