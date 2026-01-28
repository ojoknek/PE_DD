# PDF表抽出プログラム

PDFファイルから表データを抽出してCSVファイルに変換するプログラムです。

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

## 使用方法

### 基本的な使い方

```bash
python pdf_table_extractor.py input.pdf
```

このコマンドを実行すると、`input.pdf`と同じディレクトリにCSVファイルが生成されます。

### 出力ディレクトリを指定する場合

```bash
python pdf_table_extractor.py input.pdf -o output/
```

または

```bash
python pdf_table_extractor.py input.pdf --output-dir output/
```

### 出力ファイル名

- 表が1つの場合: `{PDF名}_table.csv`
- 表が複数の場合: `{PDF名}_page{ページ番号}_table{表番号}.csv`

## 機能

- PDFファイルから表を自動検出
- 複数ページのPDFに対応
- 1ページに複数の表がある場合も対応
- 空の行や列を自動的に削除
- UTF-8 BOM付きCSVで保存（Excelでも開きやすい）

## 依存パッケージ

- `pdfplumber`: PDFから表を抽出するライブラリ
- `pandas`: データ処理とCSV出力用

## 注意事項

- PDFの表が複雑なレイアウトの場合、正しく抽出できない場合があります
- 画像として埋め込まれている表は抽出できません
- PDFの品質によっては、表の認識精度が低下する場合があります
