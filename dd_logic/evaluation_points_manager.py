"""
論点管理システム
"""
from typing import Dict, List, Optional
import json
from pathlib import Path


class EvaluationPointsManager:
    """
    評価論点を管理するクラス
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        初期化
        
        Args:
            config_path: 設定ファイルのパス
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
        デフォルト設定を返す
        """
        return {
            'nn_dd': {
                'business_overview': {
                    'weight': 0.2,
                    'sub_points': [
                        '事業内容の明確性',
                        '市場規模・成長性',
                        'ビジネスモデル'
                    ]
                },
                'financial_info': {
                    'weight': 0.25,
                    'sub_points': [
                        '売上規模',
                        '成長率',
                        '収益性',
                        '財務健全性'
                    ]
                },
                'management_team': {
                    'weight': 0.2,
                    'sub_points': [
                        '経営陣の経験・実績',
                        '組織体制',
                        '人材構成'
                    ]
                },
                'market_competition': {
                    'weight': 0.15,
                    'sub_points': [
                        '市場ポジション',
                        '競合優位性',
                        '市場成長性'
                    ]
                },
                'investment_terms': {
                    'weight': 0.2,
                    'sub_points': [
                        '投資規模',
                        'バリュエーション',
                        '投資期間',
                        '出口戦略'
                    ]
                }
            },
            'im_dd': {
                'business_evaluation': {
                    'weight': 0.25,
                    'sub_points': [
                        '事業モデルの持続可能性',
                        '競合優位性（MOAT）',
                        '市場ポジション',
                        '成長戦略'
                    ]
                },
                'financial_evaluation': {
                    'weight': 0.3,
                    'sub_points': [
                        '財務諸表の分析',
                        '収益性の評価',
                        '財務健全性',
                        '将来予測の妥当性'
                    ]
                },
                'management_evaluation': {
                    'weight': 0.15,
                    'sub_points': [
                        '経営陣の能力・実績',
                        '組織体制',
                        'ガバナンス'
                    ]
                },
                'risk_evaluation': {
                    'weight': 0.15,
                    'sub_points': [
                        '事業リスク',
                        '財務リスク',
                        '法的リスク',
                        '市場リスク'
                    ]
                },
                'investment_terms_evaluation': {
                    'weight': 0.15,
                    'sub_points': [
                        'バリュエーションの妥当性',
                        '投資条件の妥当性',
                        '出口戦略の実現可能性'
                    ]
                }
            }
        }
    
    def get_evaluation_points(self, workflow_type: str) -> Dict:
        """
        評価論点を取得
        
        Args:
            workflow_type: ワークフロータイプ（'nn_dd' または 'im_dd'）
        
        Returns:
            評価論点の辞書
        """
        return self.evaluation_points.get(workflow_type, {})
    
    def get_point_weight(self, workflow_type: str, point_name: str) -> float:
        """
        論点の重みを取得
        
        Args:
            workflow_type: ワークフロータイプ
            point_name: 論点名
        
        Returns:
            重み
        """
        points = self.get_evaluation_points(workflow_type)
        if point_name in points:
            return points[point_name].get('weight', 0.0)
        return 0.0
    
    def get_sub_points(self, workflow_type: str, point_name: str) -> List[str]:
        """
        サブ論点を取得
        
        Args:
            workflow_type: ワークフロータイプ
            point_name: 論点名
        
        Returns:
            サブ論点のリスト
        """
        points = self.get_evaluation_points(workflow_type)
        if point_name in points:
            return points[point_name].get('sub_points', [])
        return []
    
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
    
    def update_point_weight(self, workflow_type: str, point_name: str, weight: float):
        """
        論点の重みを更新
        
        Args:
            workflow_type: ワークフロータイプ
            point_name: 論点名
            weight: 新しい重み
        """
        if workflow_type not in self.evaluation_points:
            self.evaluation_points[workflow_type] = {}
        
        if point_name not in self.evaluation_points[workflow_type]:
            self.evaluation_points[workflow_type][point_name] = {}
        
        self.evaluation_points[workflow_type][point_name]['weight'] = weight
