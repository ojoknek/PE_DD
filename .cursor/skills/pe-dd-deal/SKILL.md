---
name: pe-dd-deal
description: Manages PE deal folders and DD execution. Creates new deals from template (dd_logic/template_deal/ -> deals/[deal_name]/), lists deals, and runs NN/IM/LBO DD per deal. Use when the user asks to create a deal, list deals, or run deal:process (full or partial DD).
---

# 案件管理・DD実行

## トリガー
- 新規案件作成、案件一覧、案件のDD一括実行を依頼されたとき
- `/deal:create`、`/deal:list`、`/deal:process` 相当の作業

## 擬似コマンド対応

| コマンド | 対応アクション |
|----------|----------------|
| `/deal:create` | 新規案件フォルダを `dd_logic/template_deal/` をコピーして `deals/[deal_name]/` に作成 |
| `/deal:list` | `deals/` 配下の案件一覧を表示 |
| `/deal:open` | 指定案件を開く（パス・README の案内） |
| `/deal:process [deal_name]` | 当該案件で NN DD → IM DD → LBO DD を順に実行 |
| `/deal:process_nn [deal_name]` | 当該案件で NN DD のみ実行 |
| `/deal:process_im [deal_name]` | 当該案件で IM DD のみ実行 |
| `/deal:process_lbo [deal_name]` | 当該案件で LBO DD のみ実行 |

## 新規案件の作成手順
1. `dd_logic/template_deal/` をそのままコピーする
2. コピー先を `deals/[deal_name]/` とする（[deal_name] は案件名）
3. 必要に応じて以下に資料を配置する旨を案内
   - **vdr/nn/** … NN関連VDR資料
   - **vdr/im/** … IM関連VDR資料
   - **vdr/memo/** … メモ・補足資料
4. テンプレート構造: **ai_dd_results/** はAIによるDD結果の出力先、**human_dd_note/** は人間によるDDノート・追加DDの保存先（`dd_logic/template_deal/README.md` 参照）

## DD実行前: PDF→PNG変換（未変換の場合のみ執行）
- **NN DD / IM DD / LBO DD を実行する前に**、当該案件の `vdr/nn/` および `vdr/im/` を走査する
- 各フォルダ内の **PDF について**、同じフォルダに `{PDFのベース名}_page0001.png` が **無ければ** 未変換とみなす
- 未変換の PDF には、以下を **執行する**
  - `program/pdf_table_extractor.py` を実行する（出力先指定なし＝PDF と同じフォルダに PNG を保存）
  - 未変換のみ変換したい場合は `--ensure` オプションを付与: `python program/pdf_table_extractor.py <PDFパス> --ensure`
- 既に `_page0001.png` が存在する PDF はスキップしてよい
- 上記の変換処理を終えてから、NN DD → IM DD → LBO DD の各ワークフローを実行する

## DD実行時の前提
- 各DD種別は対応するスキル（pe-dd-nn / pe-dd-im / pe-dd-lbo）のワークフローに従う（`.cursor/skills/pe-dd-*/workflow.md`）
- 計算ロジックは `dd_logic/` の数式仕様書を参照して適用する

## 参照
- テンプレート構成: `dd_logic/template_deal/README.md`
- コマンド一覧: `.cursor/skills/pe-dd-deal/commands.md`
- PDF→PNG変換: `program/pdf_table_extractor.py`（`--ensure` で未変換のみ執行）
