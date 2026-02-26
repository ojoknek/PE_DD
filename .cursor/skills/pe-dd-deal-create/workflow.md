# 新規案件フォルダ作成ワークフロー

## 概要
`dd_logic/template_deal/` を `deals/` に複製し、指定された会社名でタイトル・プレースホルダーを更新する。

## 入力
- **会社名**（必須）: ユーザーが指定した会社名（例: 株式会社天山、ABC株式会社）

## 処理ステップ

### Step 1: テンプレートをコピー
```bash
cp -r dd_logic/template_deal deals/[company_name]
```
- `[company_name]` はユーザー指定の会社名（そのままディレクトリ名に使用）

### Step 2: プレースホルダー置換
`deals/[company_name]/` 配下の全 `.md` ファイルで:
- `[deal_name]` → `[company_name]` に一括置換

対象ファイル例: `README.md`, `vdr/README.md`, `vdr/nn/README.md`, `vdr/im/README.md` など

### Step 3: README タイトル・概要の更新
`deals/[company_name]/README.md` を編集:

| 変更前 | 変更後 |
|--------|--------|
| `# 案件テンプレート` | `# 案件: [company_name]` |
| `新規案件を作成する際のテンプレートです。このテンプレートをコピーして、各投資案件のディレクトリを作成します。` | `[company_name] の投資案件です。このディレクトリでNN DD・IM DD・LBO DDを実行します。` |

### Step 4: 完了案内
ユーザーに以下を伝える:
- 作成パス: `deals/[company_name]/`
- 次のステップ: `vdr/nn/`, `vdr/im/` にVDR資料を配置後、DDワークフローを実行

## 出力
- `deals/[company_name]/` ディレクトリ（テンプレート構造 + 会社名反映済み）
