#!/usr/bin/env python3
"""
PDFから表データを抽出してCSVファイルに変換するプログラム
"""

import argparse
import sys
import os
from pathlib import Path
import pdfplumber
import pandas as pd


def extract_tables_from_pdf(pdf_path: str, output_dir: str = None) -> list:
    """
    PDFファイルから表を抽出する
    
    Args:
        pdf_path: PDFファイルのパス
        output_dir: 出力ディレクトリ（指定しない場合はPDFと同じディレクトリ）
    
    Returns:
        抽出された表のリスト（DataFrameのリスト）
    """
    pdf_path = Path(pdf_path)
    
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDFファイルが見つかりません: {pdf_path}")
    
    if output_dir is None:
        output_dir = pdf_path.parent
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    
    tables = []
    
    print(f"PDFファイルを読み込んでいます: {pdf_path}")
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"総ページ数: {len(pdf.pages)}")
        
        for page_num, page in enumerate(pdf.pages, start=1):
            print(f"ページ {page_num} を処理中...")
            
            # ページから表を抽出
            page_tables = page.extract_tables()
            
            if page_tables:
                print(f"  ページ {page_num} で {len(page_tables)} 個の表を検出しました")
                
                for table_num, table in enumerate(page_tables, start=1):
                    if table and len(table) > 0:
                        # 表をDataFrameに変換
                        df = pd.DataFrame(table[1:], columns=table[0] if table[0] else None)
                        
                        # 空の行や列を削除
                        df = df.dropna(how='all').dropna(axis=1, how='all')
                        
                        if not df.empty:
                            tables.append({
                                'page': page_num,
                                'table_num': table_num,
                                'dataframe': df
                            })
                            print(f"    表 {table_num}: {df.shape[0]} 行 × {df.shape[1]} 列")
    
    return tables


def save_tables_to_csv(tables: list, pdf_path: str, output_dir: str = None):
    """
    抽出した表をCSVファイルに保存する
    
    Args:
        tables: 抽出された表のリスト
        pdf_path: 元のPDFファイルのパス
        output_dir: 出力ディレクトリ
    """
    pdf_path = Path(pdf_path)
    pdf_name = pdf_path.stem
    
    if output_dir is None:
        output_dir = pdf_path.parent
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    
    if not tables:
        print("警告: 抽出された表がありません。")
        return
    
    print(f"\n{len(tables)} 個の表をCSVファイルに保存します...")
    
    for idx, table_info in enumerate(tables, start=1):
        page = table_info['page']
        table_num = table_info['table_num']
        df = table_info['dataframe']
        
        # CSVファイル名を生成
        if len(tables) == 1:
            csv_filename = f"{pdf_name}_table.csv"
        else:
            csv_filename = f"{pdf_name}_page{page}_table{table_num}.csv"
        
        csv_path = output_dir / csv_filename
        
        # CSVファイルに保存
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f"  保存: {csv_path} ({df.shape[0]} 行 × {df.shape[1]} 列)")


def main():
    parser = argparse.ArgumentParser(
        description='PDFファイルから表データを抽出してCSVファイルに変換します',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python pdf_table_extractor.py input.pdf
  python pdf_table_extractor.py input.pdf -o output/
  python pdf_table_extractor.py input.pdf --output-dir output/
        """
    )
    
    parser.add_argument(
        'pdf_path',
        type=str,
        help='入力PDFファイルのパス'
    )
    
    parser.add_argument(
        '-o', '--output-dir',
        type=str,
        default=None,
        help='出力ディレクトリ（指定しない場合はPDFと同じディレクトリ）'
    )
    
    args = parser.parse_args()
    
    try:
        # 表を抽出
        tables = extract_tables_from_pdf(args.pdf_path, args.output_dir)
        
        # CSVファイルに保存
        save_tables_to_csv(tables, args.pdf_path, args.output_dir)
        
        print(f"\n処理が完了しました。")
        
    except FileNotFoundError as e:
        print(f"エラー: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"エラーが発生しました: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
