"""
IM DD用財務諸表抽出モジュール

PDFから財務諸表（BS、PL、CF）を詳細に抽出します。
NN DDより詳細で正確な抽出を行います。
"""
import re
from typing import Dict, List, Optional, Any
from pathlib import Path
import logging

from dd_logic.common.pdf_parser import PDFParser

logger = logging.getLogger(__name__)


class FinancialStatementExtractor:
    """財務諸表抽出クラス"""
    
    # 財務諸表の識別キーワード
    STATEMENT_KEYWORDS = {
        'balance_sheet': ['貸借対照表', 'バランスシート', 'Balance Sheet', 'BS', 'B/S'],
        'income_statement': ['損益計算書', 'Income Statement', 'Profit and Loss', 'PL', 'P/L', '損益'],
        'cash_flow': ['キャッシュフロー', 'Cash Flow', 'CF', 'C/F', '資金繰り'],
    }
    
    def __init__(self, pdf_path: str):
        """
        FinancialStatementExtractorを初期化
        
        Args:
            pdf_path: PDFファイルのパス
        """
        self.pdf_path = pdf_path
        self.parser = PDFParser(pdf_path)
    
    def extract_all_statements(self) -> Dict[str, Any]:
        """
        全ての財務諸表を抽出
        
        Returns:
            抽出した財務諸表の辞書
            {
                'balance_sheet': {...},
                'income_statement': {...},
                'cash_flow': {...}
            }
        """
        result = {
            'balance_sheet': None,
            'income_statement': None,
            'cash_flow': None
        }
        
        try:
            # 各財務諸表を抽出
            result['balance_sheet'] = self.extract_balance_sheet()
            result['income_statement'] = self.extract_income_statement()
            result['cash_flow'] = self.extract_cash_flow()
            
            logger.info("財務諸表抽出完了")
            return result
            
        except Exception as e:
            logger.error(f"財務諸表抽出エラー: {e}")
            return result
        finally:
            self.parser.close()
    
    def extract_balance_sheet(self) -> Optional[Dict[str, Any]]:
        """
        貸借対照表（BS）を抽出
        
        Returns:
            貸借対照表のデータ（見つからない場合はNone）
        """
        return self._extract_statement('balance_sheet')
    
    def extract_income_statement(self) -> Optional[Dict[str, Any]]:
        """
        損益計算書（PL）を抽出
        
        Returns:
            損益計算書のデータ（見つからない場合はNone）
        """
        return self._extract_statement('income_statement')
    
    def extract_cash_flow(self) -> Optional[Dict[str, Any]]:
        """
        キャッシュフロー計算書（CF）を抽出
        
        Returns:
            キャッシュフロー計算書のデータ（見つからない場合はNone）
        """
        return self._extract_statement('cash_flow')
    
    def _extract_statement(self, statement_type: str) -> Optional[Dict[str, Any]]:
        """
        指定された財務諸表を抽出
        
        Args:
            statement_type: 財務諸表のタイプ（'balance_sheet', 'income_statement', 'cash_flow'）
        
        Returns:
            財務諸表のデータ（見つからない場合はNone）
        """
        keywords = self.STATEMENT_KEYWORDS.get(statement_type, [])
        if not keywords:
            return None
        
        # キーワードを含む表を検索
        matched_tables = self.parser.find_tables_with_keywords(keywords)
        
        if not matched_tables:
            logger.warning(f"{statement_type}が見つかりませんでした")
            return None
        
        # 最初に見つかった表を処理
        table_data = matched_tables[0]['table']
        
        # 表を構造化データに変換
        structured_data = self._structure_table(table_data, statement_type)
        
        return {
            'type': statement_type,
            'page': matched_tables[0]['page'],
            'data': structured_data,
            'raw_table': table_data
        }
    
    def _structure_table(
        self, 
        table: List[List[str]], 
        statement_type: str
    ) -> Dict[str, Any]:
        """
        表を構造化データに変換
        
        Args:
            table: 表データ（2次元リスト）
            statement_type: 財務諸表のタイプ
        
        Returns:
            構造化されたデータ
        """
        if not table:
            return {}
        
        # ヘッダー行を特定（通常は最初の行）
        header_row = table[0] if table else []
        
        # データ行を処理
        structured = {}
        
        for row in table[1:]:
            if not row or len(row) < 2:
                continue
            
            # 最初の列が項目名、残りが数値
            item_name = str(row[0]).strip() if row[0] else ""
            if not item_name:
                continue
            
            # 数値を抽出
            values = []
            for cell in row[1:]:
                if cell:
                    value = self._extract_number_from_cell(str(cell))
                    values.append(value)
            
            # 項目名を正規化
            normalized_name = self._normalize_item_name(item_name)
            
            if normalized_name:
                structured[normalized_name] = {
                    'label': item_name,
                    'values': values,
                    'latest_value': values[0] if values else None
                }
        
        return structured
    
    def _normalize_item_name(self, item_name: str) -> Optional[str]:
        """
        項目名を正規化
        
        Args:
            item_name: 元の項目名
        
        Returns:
            正規化された項目名（マッピングできない場合はNone）
        """
        item_name_lower = item_name.lower()
        
        # よくある項目名のマッピング
        mappings = {
            # 貸借対照表
            '現金': 'cash',
            '預金': 'deposits',
            '売掛金': 'accounts_receivable',
            '在庫': 'inventory',
            '固定資産': 'fixed_assets',
            '有利子負債': 'interest_bearing_debt',
            '買掛金': 'accounts_payable',
            '純資産': 'equity',
            '自己資本': 'equity',
            
            # 損益計算書
            '売上高': 'revenue',
            '売上': 'revenue',
            '売上原価': 'cost_of_sales',
            '営業利益': 'operating_income',
            '経常利益': 'ordinary_income',
            '当期純利益': 'net_income',
            'ebitda': 'ebitda',
            'EBITDA': 'ebitda',
            
            # キャッシュフロー
            '営業CF': 'operating_cf',
            '投資CF': 'investing_cf',
            '財務CF': 'financing_cf',
            'フリーキャッシュフロー': 'free_cash_flow',
            'FCF': 'free_cash_flow',
        }
        
        # 完全一致をチェック
        if item_name in mappings:
            return mappings[item_name]
        
        # 部分一致をチェック
        for key, value in mappings.items():
            if key in item_name:
                return value
        
        # マッピングできない場合は元の名前を小文字にして返す
        return item_name_lower.replace(' ', '_').replace('　', '_')
    
    def _extract_number_from_cell(self, cell: str) -> Optional[float]:
        """
        セルから数値を抽出
        
        Args:
            cell: セルの文字列
        
        Returns:
            抽出した数値（見つからない場合はNone）
        """
        # カンマや括弧を除去
        cell = cell.replace(',', '').replace('(', '').replace(')', '')
        
        # 数値パターンを検索
        patterns = [
            r'([\d]+\.?\d*)',  # 基本的な数値
            r'([\d]+\.?\d*)\s*百万',  # 百万円単位
            r'([\d]+\.?\d*)\s*億',  # 億円単位
        ]
        
        for pattern in patterns:
            match = re.search(pattern, cell)
            if match:
                try:
                    value = float(match.group(1))
                    # 億円の場合は100倍
                    if '億' in cell:
                        value *= 100
                    return value
                except ValueError:
                    continue
        
        return None


def extract_financial_statements(pdf_path: str) -> Dict[str, Any]:
    """
    PDFから財務諸表を抽出する簡易関数
    
    Args:
        pdf_path: PDFファイルのパス
    
    Returns:
        抽出した財務諸表の辞書
    """
    extractor = FinancialStatementExtractor(pdf_path)
    return extractor.extract_all_statements()
