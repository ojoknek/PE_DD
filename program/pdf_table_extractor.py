#!/usr/bin/env python3
"""
PDFを全ページPNG画像として書き出すプログラム。
書き出したPNGは元のPDFがあるフォルダに保存します。

PE DDプロセスでの利用:
  DD実行前に、vdr/nn/ および vdr/im/ 内の各PDFについて、
  同じフォルダに {PDFのベース名}_page0001.png が無ければ未変換とみなし、
  本スクリプトを実行する（未変換のPDFのみ変換する場合は ensure_pdf_to_png を使用）。
"""

import argparse
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print(
        "エラー: PyMuPDF がインストールされていません。",
        file=sys.stderr,
    )
    print(
        "  pip install pymupdf を実行してください。",
        file=sys.stderr,
    )
    print(
        "  SSLエラーが出る場合: pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org pymupdf",
        file=sys.stderr,
    )
    sys.exit(1)


def is_png_converted(pdf_path: str) -> bool:
    """
    PDFが既にPNGに変換済みかどうかを判定する。
    同じフォルダに {PDFのベース名}_page0001.png が存在すれば変換済みとみなす。

    Args:
        pdf_path: PDFファイルのパス

    Returns:
        変換済みなら True、未変換なら False
    """
    p = Path(pdf_path)
    if not p.suffix.lower() == ".pdf":
        return False
    first_png = p.parent / f"{p.stem}_page0001.png"
    return first_png.exists()


def ensure_pdf_to_png(
    pdf_path: str,
    output_dir: str = None,
    dpi: int = 150,
    prefix: str = None,
) -> list:
    """
    PDFが未変換の場合のみPNGに書き出す（PE DDプロセス用）。
    既に同じフォルダに {ベース名}_page0001.png がある場合は何もしない。

    Args:
        pdf_path: PDFファイルのパス
        output_dir: 出力ディレクトリ（Noneの場合はPDFがあるフォルダ）
        dpi: 解像度
        prefix: 出力ファイル名のプレフィックス（Noneの場合はPDFのベース名）

    Returns:
        保存したPNGのパスリスト（既に変換済みの場合は空リスト）
    """
    if is_png_converted(pdf_path):
        return []
    return pdf_to_png(pdf_path, output_dir=output_dir, dpi=dpi, prefix=prefix)


def pdf_to_png(
    pdf_path: str,
    output_dir: str = None,
    dpi: int = 150,
    prefix: str = None,
    start_page: int = None,
    end_page: int = None,
) -> list:
    """
    PDFの全ページをPNG画像として保存する。
    出力先を指定しない場合、元のPDFがあるフォルダに保存する。

    Args:
        pdf_path: PDFファイルのパス
        output_dir: 出力ディレクトリ（指定しない場合はPDFがあるフォルダ）
        dpi: 解像度（デフォルト150）
        prefix: 出力ファイル名のプレフィックス（指定しない場合はPDFのベース名）
        start_page: 開始ページ（1始まり、省略時は1）
        end_page: 終了ページ（1始まり、省略時は最終ページ）

    Returns:
        保存したPNGファイルのパスリスト
    """
    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDFファイルが見つかりません: {pdf_path}")

    # 指定がなければPDFがあるフォルダに保存
    if output_dir is None:
        output_dir = pdf_path.parent
    else:
        output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    prefix = prefix or pdf_path.stem
    saved_paths = []

    # 72 DPI が PDF のデフォルトなので、指定 DPI にする倍率
    zoom = dpi / 72
    matrix = fitz.Matrix(zoom, zoom)

    print(f"PDFを読み込んでいます: {pdf_path}")

    doc = fitz.open(pdf_path)
    try:
        total = len(doc)
        start = (start_page - 1) if start_page is not None else 0
        end = end_page if end_page is not None else total
        end = min(end, total)
        start = max(0, min(start, total - 1))

        print(f"総ページ数: {total}（{start + 1} ～ {end} を出力）")
        print(f"出力先: {output_dir}")

        for page_num in range(start, end):
            page = doc[page_num]
            pix = page.get_pixmap(matrix=matrix, alpha=False)
            out_name = f"{prefix}_page{page_num + 1:04d}.png"
            out_path = output_dir / out_name
            pix.save(str(out_path))
            saved_paths.append(out_path)
            print(f"  保存: {out_path}")
    finally:
        doc.close()

    return saved_paths


def main():
    parser = argparse.ArgumentParser(
        description="PDFの全ページをPNG画像として書き出します（出力先は元のPDFがあるフォルダ）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python pdf_table_extractor.py input.pdf
    → input.pdf と同じフォルダに PNG を保存
  python pdf_table_extractor.py input.pdf -o other/
    → other/ に保存
  python pdf_table_extractor.py input.pdf --dpi 200
  python pdf_table_extractor.py input.pdf --start 1 --end 10
        """,
    )

    parser.add_argument("pdf_path", type=str, help="入力PDFファイルのパス")

    parser.add_argument(
        "-o",
        "--output-dir",
        type=str,
        default=None,
        help="出力ディレクトリ（指定しない場合はPDFがあるフォルダ）",
    )

    parser.add_argument(
        "--dpi",
        type=int,
        default=150,
        metavar="N",
        help="解像度（デフォルト: 150）",
    )

    parser.add_argument(
        "--prefix",
        type=str,
        default=None,
        help="出力ファイル名のプレフィックス（デフォルト: PDFのファイル名）",
    )

    parser.add_argument(
        "--start",
        type=int,
        default=None,
        metavar="N",
        help="開始ページ（1始まり）",
    )

    parser.add_argument(
        "--end",
        type=int,
        default=None,
        metavar="N",
        help="終了ページ（1始まり、このページまで含む）",
    )

    parser.add_argument(
        "--ensure",
        action="store_true",
        help="未変換の場合のみ実行（同じフォルダに _page0001.png が無いときだけ変換。PE DDプロセスで使用）",
    )

    args = parser.parse_args()

    try:
        if args.ensure:
            paths = ensure_pdf_to_png(
                args.pdf_path,
                output_dir=args.output_dir,
                dpi=args.dpi,
                prefix=args.prefix,
            )
            if paths:
                print(f"\n処理が完了しました。（{len(paths)} 枚のPNGを保存）")
            else:
                print("\n既にPNGに変換済みのためスキップしました。")
        else:
            paths = pdf_to_png(
                args.pdf_path,
                output_dir=args.output_dir,
                dpi=args.dpi,
                prefix=args.prefix,
                start_page=args.start,
                end_page=args.end,
            )
            print(f"\n処理が完了しました。（{len(paths)} 枚のPNGを保存）")
    except FileNotFoundError as e:
        print(f"エラー: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"エラーが発生しました: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
