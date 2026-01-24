"""
IM DD用抽出モジュール

詳細な財務諸表抽出機能を提供します。
"""
from .financial_statement_extractor import (
    FinancialStatementExtractor,
    extract_financial_statements
)

__all__ = ['FinancialStatementExtractor', 'extract_financial_statements']
