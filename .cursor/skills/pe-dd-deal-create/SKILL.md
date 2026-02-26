---
name: pe-dd-deal-create
description: Creates a new PE deal folder from template. Copies dd_logic/template_deal/ to deals/[company_name]/, replaces [deal_name] with the specified company name, and updates the README title. Use when the user asks to create a new deal, add a new company/deal, or set up a draft deal folder.
---

# 新規案件フォルダ作成

## トリガー
- 新規案件の作成、新しい会社のdealフォルダを作りたいとき
- 「〇〇のdealを作って」「新規案件を追加して」など

## 実行手順

1. **会社名を確認**  
   ユーザーが指定した会社名（例: 株式会社天山）を `[company_name]` とする

2. **テンプレートをコピー**
   ```bash
   cp -r dd_logic/template_deal deals/[company_name]
   ```

3. **プレースホルダーを置換**  
   コピー先 `deals/[company_name]/` 内の全ファイルで:
   - `[deal_name]` → `[company_name]` に置換

4. **READMEのタイトルを更新**  
   `deals/[company_name]/README.md` の先頭を:
   - 「# 案件テンプレート」→「# 案件: [company_name]」
   - 「概要」の「新規案件を作成する際のテンプレートです...」→「[company_name] の投資案件です。このディレクトリでDDを実行します。」

5. **完了案内**  
   作成したパスと、次のステップ（vdr/nn/, vdr/im/ への資料配置）を案内する

## 参照
- テンプレート: `dd_logic/template_deal/`
- 案件一覧: `deals/README.md`
