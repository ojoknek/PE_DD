# agents/ ディレクトリ（廃止予定）

## 状態
**本ディレクトリの内容は `.cursor/skills/` および `dd_logic/template_deal/` に移管済みです。**  
参照がすべて移行先を指すよう更新済みのため、**このディレクトリは削除して問題ありません。**

## 移管先

| 旧パス（agents/） | 移管先 |
|-------------------|--------|
| `agents/prompts/nn_dd/` | `.cursor/skills/pe-dd-nn/prompts/` |
| `agents/prompts/im_dd/` | `.cursor/skills/pe-dd-im/prompts/` |
| `agents/prompts/lbo_dd/` | `.cursor/skills/pe-dd-lbo/prompts/` |
| `agents/workflows/*.md` | 各スキル配下の `.cursor/skills/pe-dd-*/workflow.md` |
| `agents/commands/README.md` | `.cursor/skills/pe-dd-deal/commands.md` |
| `agents/template_deal/` | **`dd_logic/template_deal/`** |

## 削除方法
プロジェクトルートで以下を実行すると、agents/ を削除できます。

```bash
rm -rf agents/
```

削除前に、`dd_logic/template_deal/` が存在することを確認してください（移管済み）。

## 参照
- スキル・ワークフロー・プロンプト: `.cursor/skills/README.md`
- 案件テンプレート: `dd_logic/template_deal/README.md`
