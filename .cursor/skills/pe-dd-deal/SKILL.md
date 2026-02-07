---
name: pe-dd-deal
description: Manages PE deal folders and DD execution. Creates new deals from template (agents/template_deal/ -> deals/[deal_name]/), lists deals, and runs NN/IM/LBO DD per deal. Use when the user asks to create a deal, list deals, or run deal:process (full or partial DD).
---

# 案件管理・DD実行

## トリガー
- 新規案件作成、案件一覧、案件のDD一括実行を依頼されたとき
- `/deal:create`、`/deal:list`、`/deal:process` 相当の作業

## 擬似コマンド対応

| コマンド | 対応アクション |
|----------|----------------|
| `/deal:create` | 新規案件フォルダを `agents/template_deal/` をコピーして `deals/[deal_name]/` に作成 |
| `/deal:list` | `deals/` 配下の案件一覧を表示 |
| `/deal:open` | 指定案件を開く（パス・README の案内） |
| `/deal:process [deal_name]` | 当該案件で NN DD → IM DD → LBO DD を順に実行 |
| `/deal:process_nn [deal_name]` | 当該案件で NN DD のみ実行 |
| `/deal:process_im [deal_name]` | 当該案件で IM DD のみ実行 |
| `/deal:process_lbo [deal_name]` | 当該案件で LBO DD のみ実行 |

## 新規案件の作成手順
1. `agents/template_deal/` をそのままコピーする
2. コピー先を `deals/[deal_name]/` とする（[deal_name] は案件名）
3. 必要に応じて以下に資料を配置する旨を案内
   - **vdr/nn/** … NN関連VDR資料
   - **vdr/im/** … IM関連VDR資料
   - **vdr/memo/** … メモ・補足資料
4. テンプレート構造: **ai_dd_results/** はAIによるDD結果の出力先、**human_dd_note/** は人間によるDDノート・追加DDの保存先（`agents/template_deal/README.md` 参照）

## DD実行時の前提
- 各DD種別は対応するスキル（pe-dd-nn / pe-dd-im / pe-dd-lbo）のワークフローに従う
- 計算ロジックは `dd_logic/` の数式仕様書を参照して適用する

## 参照
- テンプレート構成: `agents/template_deal/README.md`
- コマンド一覧: `agents/commands/README.md`
