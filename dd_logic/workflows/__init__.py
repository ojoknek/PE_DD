"""
統合ワークフローモジュール

案件処理の統合ワークフローを提供します。
"""
from .deal_processor import DealProcessor, process_deal

__all__ = ['DealProcessor', 'process_deal']
