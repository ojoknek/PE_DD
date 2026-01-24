"""
NN DD用簡易PDF数値抽出モジュール

PDFから表を検出し、基本的な財務数値を抽出します。
IM DDより簡易で、ラフな数値抽出でOKです。
"""
import re
from typing import Dict, Optional, List, Any
from pathlib import Path
import logging

from dd_logic.common.pdf_parser import PDFParser

logger = logging.getLogger(__name__)


class SimpleFinancialExtractor:
    """簡易財務数値抽出クラス"""
    
    # 抽出対象のキーワードマッピング
    KEYWORD_MAPPINGS = {
        'sales': ['売上', '売上高', 'revenue', 'sales', '売上金額', '総売上'],
        'adj_ebitda': ['調整後ebitda', 'adj ebitda', 'adjusted ebitda', 'ebitda', 'EBITDA', '調整EBITDA'],
        'net_debt': ['net debt', '純有利子負債', 'ネットデット', 'Net Debt', '純負債'],
        'ebitda_multiple': ['ebitda倍率', 'ebitda multiple', 'EBITDA倍率', '倍率', 'multiple'],
    }
    
    def __init__(self, pdf_path: str):
        """
        SimpleFinancialExtractorを初期化
        
        Args:
            pdf_path: PDFファイルのパス
        """
        self.pdf_path = pdf_path
        self.parser = PDFParser(pdf_path)
    
    def extract_financial_data(self) -> Dict[str, Optional[float]]:
        """
        基本的な財務数値を抽出
        
        Returns:
            抽出した財務数値の辞書
            {
                'sales': float or None,
                'adj_ebitda': float or None,
                'net_debt': float or None,
                'ebitda_multiple': float or None
            }
        """
        result = {
            'sales': None,
            'adj_ebitda': None,
            'net_debt': None,
            'ebitda_multiple': None
        }
        
        try:
            # 全ページから表を抽出
            tables = self.parser.extract_tables()
            
            # テキストも抽出（表にない場合のフォールバック）
            text = self.parser.extract_text()
            
            # 各数値を抽出
            for key, keywords in self.KEYWORD_MAPPINGS.items():
                value = self._extract_value_from_tables(tables, keywords)
                if value is None:
                    # 表から見つからない場合はテキストから検索
                    value = self._extract_value_from_text(text, keywords)
                result[key] = value
            
            logger.info(f"財務数値抽出完了: {result}")
            return result
            
        except Exception as e:
            logger.error(f"財務数値抽出エラー: {e}")
            return result
        finally:
            self.parser.close()
    
    def _extract_value_from_tables(
        self, 
        tables: List[List[List[str]]], 
        keywords: List[str]
    ) -> Optional[float]:
        """
        表から数値を抽出
        
        Args:
            tables: 抽出した表のリスト
            keywords: 検索キーワードのリスト
        
        Returns:
            抽出した数値（見つからない場合はNone）
        """
        for table in tables:
            if not table:
                continue
            
            # 表をフラットな文字列に変換して検索
            table_text = ' '.join([' '.join(row) for row in table if row])
            
            # キーワードが含まれているかチェック
            for keyword in keywords:
                if keyword.lower() in table_text.lower():
                    # キーワードの近くの数値を探す
                    value = self._find_nearby_number(table, keyword)
                    if value is not None:
                        return value
        
        return None
    
    def _extract_value_from_text(
        self, 
        text: str, 
        keywords: List[str]
    ) -> Optional[float]:
        """
        テキストから数値を抽出
        
        Args:
            text: 抽出したテキスト
            keywords: 検索キーワードのリスト
        
        Returns:
            抽出した数値（見つからない場合はNone）
        """
        for keyword in keywords:
            # キーワードの前後を検索
            pattern = rf'{re.escape(keyword)}[:\s]*([\d,]+\.?\d*)'
            matches = re.findall(pattern, text, re.IGNORECASE)
            
            if matches:
                # 最初に見つかった数値を返す
                value_str = matches[0].replace(',', '')
                try:
                    return float(value_str)
                except ValueError:
                    continue
        
        return None
    
    def _find_nearby_number(
        self, 
        table: List[List[str]], 
        keyword: str
    ) -> Optional[float]:
        """
        表内でキーワードの近くの数値を探す
        
        Args:
            table: 表データ（2次元リスト）
            keyword: 検索キーワード
        
        Returns:
            見つかった数値（見つからない場合はNone）
        """
        for row_idx, row in enumerate(table):
            if not row:
                continue
            
            # 行内でキーワードを検索
            row_text = ' '.join([str(cell) if cell else '' for cell in row])
            
            if keyword.lower() in row_text.lower():
                # 同じ行内の数値を探す
                for cell in row:
                    if cell:
                        value = self._extract_number_from_cell(str(cell))
                        if value is not None:
                            return value
                
                # 次の行の数値を探す（よくあるパターン）
                if row_idx + 1 < len(table):
                    next_row = table[row_idx + 1]
                    for cell in next_row:
                        if cell:
                            value = self._extract_number_from_cell(str(cell))
                            if value is not None:
                                return value
        
        return None
    
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
        
        # 数値パターンを検索（百万円単位なども考慮）
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


def extract_simple_financials(pdf_path: str) -> Dict[str, Optional[float]]:
    """
    PDFから基本的な財務数値を抽出する簡易関数
    
    Args:
        pdf_path: PDFファイルのパス
    
    Returns:
        抽出した財務数値の辞書
    """
    extractor = SimpleFinancialExtractor(pdf_path)
    return extractor.extract_financial_data()
