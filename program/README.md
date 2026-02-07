# PDF→PNG 書き出しプログラム

PDFの全ページをPNG画像として書き出すプログラムです。  
**書き出したPNGは、元のPDFがあるフォルダに保存されます。**

- **実装**: PyMuPDF (fitz) による PDF レンダリングで PNG 出力を実現
- **動作確認済み**: 案件フォルダ内の IM PDF（例: 株式会社ヌベール `vdr/im/中部_洋菓子製造_im.pdf` 21ページ）で変換・`--ensure` によるスキップを確認

## セットアップ

### 1. 仮想環境の有効化（`program` ディレクトリ内）

```bash
cd program

# macOS/Linux
source .venv/bin/activate

# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
```

### 2. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

**SSL証明書エラーでインストールに失敗する場合**（例: `SSLCertVerificationError`）:

```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

## 使用方法

### 基本的な使い方

```bash
python pdf_table_extractor.py input.pdf
```

このコマンドを実行すると、`input.pdf` がある**同じフォルダ**に、全ページ分のPNGが生成されます。

### 出力ファイル名

- `{PDFのファイル名}_page0001.png`
- `{PDFのファイル名}_page0002.png`
- …

### 出力先を別フォルダにしたい場合

```bash
python pdf_table_extractor.py input.pdf -o output/
```

または

```bash
python pdf_table_extractor.py input.pdf --output-dir output/
```

### その他のオプション

| オプション | 説明 |
|-----------|------|
| `--dpi N` | 解像度（デフォルト: 150） |
| `--prefix 名前` | 出力ファイル名のプレフィックス（デフォルト: PDFのファイル名） |
| `--start N` | 開始ページ（1始まり） |
| `--end N` | 終了ページ（1始まり、このページまで含む） |
| `--ensure` | **未変換の場合のみ執行**。同じフォルダに `_page0001.png` が無いときだけ変換する（PE DDプロセスで使用） |

例:

```bash
python pdf_table_extractor.py input.pdf --dpi 200
python pdf_table_extractor.py input.pdf --start 1 --end 10
```

### PE DDプロセスでの利用

DD実行時、案件の `vdr/nn/` および `vdr/im/` 内のPDFのうち、**まだPNGに変換されていないもの**（同じフォルダに `{PDF名}_page0001.png` が無いもの）について、本プログラムを実行する。

- 未変換のPDFのみ変換したい場合: `--ensure` を付けて実行する  
  `python pdf_table_extractor.py <PDFパス> --ensure`
- 実行後、PNGは元のPDFがあるフォルダに保存される（出力先指定なし）
- 詳細な手順は `.cursor/skills/pe-dd-deal/SKILL.md` の「DD実行前: PDF→PNG変換」を参照

## 機能

- PDFの全ページをPNG画像として書き出し（PDF→PNG 変換を実現）
- 出力先はデフォルトで**元のPDFがあるフォルダ**
- 解像度（DPI）の指定
- ページ範囲の指定（--start / --end）
- ファイル名プレフィックスの指定
- `--ensure`: 既に同じフォルダに `_page0001.png` がある場合はスキップ（冪等）

## 依存パッケージ

- `pymupdf` (PyMuPDF): PDFのレンダリングとPNG出力用（必須）。未インストールの場合はスクリプト実行時にエラーと SSL 回避の案内を表示します。

## 注意事項

- 大きなPDFや高DPI指定時は、処理に時間がかかることがあります。
- 出力先フォルダが存在しない場合は自動作成されます。
