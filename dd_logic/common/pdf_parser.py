"""
PDF解析共通モジュール

pdfplumberを使用したPDF解析の共通機能を提供します。
テキスト抽出、表抽出、基本的なPDF操作をサポートします。
"""
import pdfplumber
from typing import List, Dict, Optional, Any
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class PDFParser:
    """PDF解析の共通クラス"""
    
    def __init__(self, pdf_path: str):
        """
        PDFParserを初期化
        
        Args:
            pdf_path: PDFファイルのパス
        """
        self.pdf_path = Path(pdf_path)
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDFファイルが見つかりません: {pdf_path}")
        
        self.pdf = None
        self._open_pdf()
    
    def _open_pdf(self):
        """PDFファイルを開く"""
        try:
            self.pdf = pdfplumber.open(str(self.pdf_path))
        except Exception as e:
            logger.error(f"PDFファイルの読み込みに失敗しました: {e}")
            raise
    
    def extract_text(self) -> str:
        """
        全ページからテキストを抽出
        
        Returns:
            抽出したテキスト（全ページ結合）
        """
        if not self.pdf:
            raise RuntimeError("PDFファイルが開かれていません")
        
        text_parts = []
        for page in self.pdf.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)
        
        return "\n\n".join(text_parts)
    
    def extract_tables(self, page_num: Optional[int] = None) -> List[List[List[str]]]:
        """
        表を抽出
        
        Args:
            page_num: ページ番号（Noneの場合は全ページ）
        
        Returns:
            抽出した表のリスト（各表は2次元リスト）
        """
        if not self.pdf:
            raise RuntimeError("PDFファイルが開かれていません")
        
        tables = []
        pages = [self.pdf.pages[page_num]] if page_num is not None else self.pdf.pages
        
        for page in pages:
            page_tables = page.extract_tables()
            if page_tables:
                tables.extend(page_tables)
        
        return tables
    
    def extract_tables_from_page(self, page_num: int) -> List[List[List[str]]]:
        """
        指定ページから表を抽出
        
        Args:
            page_num: ページ番号（0始まり）
        
        Returns:
            抽出した表のリスト
        """
        return self.extract_tables(page_num=page_num)
    
    def get_page_count(self) -> int:
        """
        ページ数を取得
        
        Returns:
            ページ数
        """
        if not self.pdf:
            raise RuntimeError("PDFファイルが開かれていません")
        return len(self.pdf.pages)
    
    def extract_text_from_page(self, page_num: int) -> str:
        """
        指定ページからテキストを抽出
        
        Args:
            page_num: ページ番号（0始まり）
        
        Returns:
            抽出したテキスト
        """
        if not self.pdf:
            raise RuntimeError("PDFファイルが開かれていません")
        
        if page_num < 0 or page_num >= len(self.pdf.pages):
            raise ValueError(f"無効なページ番号: {page_num}")
        
        page = self.pdf.pages[page_num]
        return page.extract_text() or ""
    
    def find_tables_with_keywords(self, keywords: List[str]) -> List[Dict[str, Any]]:
        """
        キーワードを含む表を検索
        
        Args:
            keywords: 検索キーワードのリスト
        
        Returns:
            キーワードを含む表の情報リスト
            [{"page": int, "table": List[List[str]], "matched_keywords": List[str]}]
        """
        if not self.pdf:
            raise RuntimeError("PDFファイルが開かれていません")
        
        results = []
        
        for page_num, page in enumerate(self.pdf.pages):
            # ページのテキストを取得
            page_text = page.extract_text() or ""
            
            # キーワードがページ内にあるかチェック
            matched_keywords = [kw for kw in keywords if kw.lower() in page_text.lower()]
            
            if matched_keywords:
                # キーワードが見つかったページの表を抽出
                tables = page.extract_tables()
                for table in tables:
                    results.append({
                        "page": page_num,
                        "table": table,
                        "matched_keywords": matched_keywords
                    })
        
        return results
    
    def close(self):
        """PDFファイルを閉じる"""
        if self.pdf:
            self.pdf.close()
            self.pdf = None
    
    def __enter__(self):
        """コンテキストマネージャーのエントリ"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """コンテキストマネージャーのエグジット"""
        self.close()


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    PDFからテキストを抽出する簡易関数
    
    Args:
        pdf_path: PDFファイルのパス
    
    Returns:
        抽出したテキスト
    """
    with PDFParser(pdf_path) as parser:
        return parser.extract_text()


def extract_tables_from_pdf(pdf_path: str) -> List[List[List[str]]]:
    """
    PDFから表を抽出する簡易関数
    
    Args:
        pdf_path: PDFファイルのパス
    
    Returns:
        抽出した表のリスト
    """
    with PDFParser(pdf_path) as parser:
        return parser.extract_tables()
