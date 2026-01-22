#!/usr/bin/env python3
"""
壁の道の向こう側のブログ記事をスクレイピングするスクリプト
"""

import requests
from bs4 import BeautifulSoup
import time
import os
from pathlib import Path
import re

# 記事URLリスト（全63件）
ARTICLES = [
    # ページ1
    {"url": "https://finance-rice-field.com/dcf-excel", "title": "DCF法の計算方法は？Excelでの計算式をわかりやすく徹底解説", "date": "2025-01-30"},
    {"url": "https://finance-rice-field.com/entry-model", "title": "財務モデリング＜入門編＞をリリースしました", "date": "2023-06-06"},
    {"url": "https://finance-rice-field.com/modeling-online-school", "title": "本格的な財務モデリングを学べるおすすめ講座を5つ厳選【独学OK】", "date": "2019-11-06"},
    {"url": "https://finance-rice-field.com/topic-debt-financing-fee", "title": "LBOモデルにおける負債発行費用の取り扱いについて", "date": "2019-04-07"},
    {"url": "https://finance-rice-field.com/topic-minimum-cash", "title": "LBOモデルでミニマムキャッシュを設定する理由", "date": "2019-04-07"},
    {"url": "https://finance-rice-field.com/modeling-topic-dilution", "title": "新株予約権や転換社債の希薄化インパクト計算方法", "date": "2019-03-17"},
    {"url": "https://finance-rice-field.com/modeling-topic-mistake-in-ebitda-and-ev", "title": "財務モデリングで間違いやすいポイント～EBITDAとEV", "date": "2019-03-11"},
    {"url": "https://finance-rice-field.com/ma-model-19", "title": "投資銀行の本格的M&Aモデル作成方法をエクセル付きで解説19", "date": "2019-03-04"},
    {"url": "https://finance-rice-field.com/ma-model-18", "title": "投資銀行の本格的M&Aモデル作成方法をエクセル付きで解説18", "date": "2019-03-01"},
    {"url": "https://finance-rice-field.com/ma-model-17", "title": "投資銀行の本格的M&Aモデル作成方法をエクセル付きで解説17", "date": "2019-02-27"},
    # ページ2
    {"url": "https://finance-rice-field.com/ma-model-16", "title": "投資銀行の本格的M&Aモデル作成方法をエクセル付きで解説16", "date": "2019-02-25"},
    {"url": "https://finance-rice-field.com/ma-model-15", "title": "投資銀行の本格的M&Aモデル作成方法をエクセル付きで解説15", "date": "2019-02-22"},
    {"url": "https://finance-rice-field.com/ma-model-14", "title": "投資銀行の本格的M&Aモデル作成方法をエクセル付きで解説14", "date": "2019-02-20"},
    {"url": "https://finance-rice-field.com/ma-model-13", "title": "投資銀行の本格的M&Aモデル作成方法をエクセル付きで解説13", "date": "2019-02-18"},
    {"url": "https://finance-rice-field.com/ma-model-12", "title": "投資銀行の本格的M&Aモデル作成方法をエクセル付きで解説12", "date": "2019-02-15"},
    {"url": "https://finance-rice-field.com/ma-model-11", "title": "投資銀行の本格的M&Aモデル作成方法をエクセル付きで解説11", "date": "2019-02-13"},
    {"url": "https://finance-rice-field.com/ma-model-10", "title": "投資銀行の本格的M&Aモデル作成方法をエクセル付きで解説10", "date": "2019-02-11"},
    {"url": "https://finance-rice-field.com/ma-model-9", "title": "投資銀行の本格的M&Aモデル作成方法をエクセル付きで解説9", "date": "2019-02-08"},
    {"url": "https://finance-rice-field.com/ma-model-8", "title": "投資銀行の本格的M&Aモデル作成方法をエクセル付きで解説8", "date": "2019-02-06"},
    {"url": "https://finance-rice-field.com/ma-model-7", "title": "投資銀行の本格的M&Aモデル作成方法をエクセル付きで解説7", "date": "2019-02-04"},
    # ページ3
    {"url": "https://finance-rice-field.com/ma-model-6", "title": "投資銀行の本格的M&Aモデル作成方法をエクセル付きで解説6", "date": "2019-02-01"},
    {"url": "https://finance-rice-field.com/ma-model-5", "title": "投資銀行の本格的M&Aモデル作成方法をエクセル付きで解説5", "date": "2019-01-30"},
    {"url": "https://finance-rice-field.com/ma-model-4", "title": "投資銀行の本格的M&Aモデル作成方法をエクセル付きで解説4", "date": "2019-01-28"},
    {"url": "https://finance-rice-field.com/ma-model-3", "title": "投資銀行の本格的M&Aモデル作成方法をエクセル付きで解説3", "date": "2019-01-25"},
    {"url": "https://finance-rice-field.com/ma-model-2", "title": "投資銀行の本格的M&Aモデル作成方法をエクセル付きで解説2", "date": "2019-01-23"},
    {"url": "https://finance-rice-field.com/ma-model-1", "title": "投資銀行の本格的M&Aモデル作成方法をエクセル付きで解説1", "date": "2019-01-21"},
    {"url": "https://finance-rice-field.com/lbo-valuation-paper-form", "title": "投資銀行の本格的LBOモデル作成方法：paper LBOモデルの解説", "date": "2018-12-14"},
    {"url": "https://finance-rice-field.com/lbo-valuation-short-form", "title": "投資銀行の本格的LBOモデル作成方法：short-form LBOモデルの解説", "date": "2018-12-13"},
    {"url": "https://finance-rice-field.com/lbo-valuation-12", "title": "投資銀行の本格的LBOモデル作成方法をエクセル付きで解説12", "date": "2018-12-09"},
    {"url": "https://finance-rice-field.com/lbo-valuation-11", "title": "投資銀行の本格的LBOモデル作成方法をエクセル付きで解説11", "date": "2018-12-08"},
    # ページ4
    {"url": "https://finance-rice-field.com/lbo-valuation-10", "title": "投資銀行の本格的LBOモデル作成方法をエクセル付きで解説10", "date": "2018-12-07"},
    {"url": "https://finance-rice-field.com/lbo-valuation-9", "title": "投資銀行の本格的LBOモデル作成方法をエクセル付きで解説9", "date": "2018-12-06"},
    {"url": "https://finance-rice-field.com/lbo-valuation-8", "title": "投資銀行の本格的LBOモデル作成方法をエクセル付きで解説8", "date": "2018-12-05"},
    {"url": "https://finance-rice-field.com/lbo-valuation-7", "title": "投資銀行の本格的LBOモデル作成方法をエクセル付きで解説7", "date": "2018-12-04"},
    {"url": "https://finance-rice-field.com/lbo-valuation-6", "title": "投資銀行の本格的LBOモデル作成方法をエクセル付きで解説6", "date": "2018-12-03"},
    {"url": "https://finance-rice-field.com/lbo-valuation-5", "title": "投資銀行の本格的LBOモデル作成方法をエクセル付きで解説5", "date": "2018-12-02"},
    {"url": "https://finance-rice-field.com/lbo-valuation-4", "title": "投資銀行の本格的LBOモデル作成方法をエクセル付きで解説4", "date": "2018-11-30"},
    {"url": "https://finance-rice-field.com/lbo-valuation-3", "title": "投資銀行の本格的LBOモデル作成方法をエクセル付きで解説3", "date": "2018-11-29"},
    {"url": "https://finance-rice-field.com/lbo-valuation-2", "title": "投資銀行の本格的LBOモデル作成方法をエクセル付きで解説2", "date": "2018-11-28"},
    {"url": "https://finance-rice-field.com/lbo-valuation-1", "title": "投資銀行の本格的LBOモデル作成方法をエクセル付きで解説1", "date": "2018-11-27"},
    # ページ5
    {"url": "https://finance-rice-field.com/cash-sweep-5", "title": "投資銀行のCash Sweepモデル：エクセル付き解説5", "date": "2018-11-21"},
    {"url": "https://finance-rice-field.com/cash-sweep-4", "title": "投資銀行のCash Sweepモデル：エクセル付き解説4", "date": "2018-11-20"},
    {"url": "https://finance-rice-field.com/cash-sweep-3", "title": "投資銀行のCash Sweepモデル：エクセル付き解説3", "date": "2018-11-19"},
    {"url": "https://finance-rice-field.com/cash-sweep-2", "title": "投資銀行のCash Sweepモデル：エクセル付き解説2", "date": "2018-11-18"},
    {"url": "https://finance-rice-field.com/cash-sweep-1", "title": "投資銀行のCash Sweepモデル：エクセル付き解説1", "date": "2018-11-17"},
    {"url": "https://finance-rice-field.com/dcf-valuation-18", "title": "DCF法：企業価値（EV）から株式価値を計算する", "date": "2018-11-16"},
    {"url": "https://finance-rice-field.com/dcf-valuation-17", "title": "exitマルチプル法と永久成長率法で企業価値を計算する方法", "date": "2018-11-15"},
    {"url": "https://finance-rice-field.com/dcf-valuation-16", "title": "DCF法：各年の企業価値の割引率を計算【エクセルでの計算方法も】", "date": "2018-11-14"},
    {"url": "https://finance-rice-field.com/dcf-valuation-15", "title": "WACCの計算方法とエクセルの活用術を解説", "date": "2018-11-13"},
    {"url": "https://finance-rice-field.com/dcf-valuation-14", "title": "DCF法：アンレバード・フリー・キャッシュフロー（FCF）を計算する方法", "date": "2018-11-13"},
    # ページ6
    {"url": "https://finance-rice-field.com/dcf-valuation-13", "title": "DCF法：将来価値を現在価値に割り引く5つのステップを概観する", "date": "2018-11-13"},
    {"url": "https://finance-rice-field.com/dcf-valuation-12", "title": "DCF法：Excelの循環参照のオン・オフスイッチを作りモデルを完成させる", "date": "2018-11-12"},
    {"url": "https://finance-rice-field.com/dcf-valuation-11", "title": "DCF法：受取・支払利息をISにリンクさせ、Excelの反復計算をオンにする", "date": "2018-11-11"},
    {"url": "https://finance-rice-field.com/dcf-valuation-10", "title": "DCF法：CFで算出した現金/短期借入金をBSにリンクさせる", "date": "2018-11-10"},
    {"url": "https://finance-rice-field.com/dcf-valuation-9", "title": "DCF法：CFを構築する方法", "date": "2018-11-10"},
    {"url": "https://finance-rice-field.com/dcf-valuation-8", "title": "DCF法：BSの各項目をキャッシュフロー計算書（CF）の項目毎（営業、投資、財務）に分類する", "date": "2018-11-09"},
    {"url": "https://finance-rice-field.com/dcf-valuation-7", "title": "DCF法：貸借対照表（BS）を構築する方法", "date": "2018-11-09"},
    {"url": "https://finance-rice-field.com/dcf-valuation-6", "title": "DCF法：負債の返済スケジュールと受取・支払利息を計算する", "date": "2018-11-08"},
    {"url": "https://finance-rice-field.com/dcf-valuation-5", "title": "エクセルを使った運転資金の計算方法と減価償却のISへリンクのさせ方", "date": "2018-11-08"},
    {"url": "https://finance-rice-field.com/dcf-valuation-4", "title": "損益計算書（IS）を構築し、IS項目の予想を立てる方法", "date": "2018-11-07"},
    # ページ7
    {"url": "https://finance-rice-field.com/dcf-valuation-3", "title": "エクセルの反復計算をオフにし循環参照を解消する", "date": "2018-11-07"},
    {"url": "https://finance-rice-field.com/dcf-valuation-2", "title": "オペレーティングモデルの概要と構築するための12ステップを解説", "date": "2018-11-06"},
    {"url": "https://finance-rice-field.com/dcf-valuation-1", "title": "企業価値算定をするためのDCF法を18ステップで解説【財務モデリングの練習問題あり】", "date": "2018-11-05"},
]

def sanitize_filename(filename):
    """ファイル名から不正な文字を削除"""
    # 不正な文字を置換
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # 長すぎる場合は切り詰め
    if len(filename) > 200:
        filename = filename[:200]
    return filename

def scrape_article(url, title, date, output_dir):
    """記事をスクレイピングしてマークダウンファイルに保存"""
    try:
        print(f"取得中: {title}")
        
        # ユーザーエージェントを設定
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # ページを取得
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        
        # BeautifulSoupで解析
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 記事本文を取得（Wordpressのarticleタグから）
        article_content = soup.find('article')
        if not article_content:
            print(f"  警告: 記事本文が見つかりません: {url}")
            return False
        
        # 記事タイトルを取得
        article_title = soup.find('h1', class_='entry-title')
        if not article_title:
            article_title = soup.find('h1')
        
        # 記事本文のコンテンツを取得
        entry_content = article_content.find(class_='entry-content')
        if not entry_content:
            entry_content = article_content
        
        # マークダウン形式で保存
        filename = sanitize_filename(f"{date}_{title}.md")
        filepath = output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            # メタデータ
            f.write(f"# {title}\n\n")
            f.write(f"- **URL**: {url}\n")
            f.write(f"- **日付**: {date}\n")
            f.write(f"- **取得日**: {time.strftime('%Y-%m-%d')}\n\n")
            f.write("---\n\n")
            
            # 本文を取得（HTMLタグを適度に保持）
            # 見出しタグの処理
            for heading in entry_content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                level = int(heading.name[1])
                heading.insert_before(f"\n{'#' * (level + 1)} ")
                heading.unwrap()
            
            # 段落の処理
            for p in entry_content.find_all('p'):
                p.insert_after('\n\n')
                p.unwrap()
            
            # リストの処理
            for ul in entry_content.find_all('ul'):
                for li in ul.find_all('li'):
                    li.insert_before('- ')
                    li.insert_after('\n')
                    li.unwrap()
                ul.insert_after('\n')
                ul.unwrap()
            
            for ol in entry_content.find_all('ol'):
                for i, li in enumerate(ol.find_all('li'), 1):
                    li.insert_before(f'{i}. ')
                    li.insert_after('\n')
                    li.unwrap()
                ol.insert_after('\n')
                ol.unwrap()
            
            # テキストを抽出
            text = entry_content.get_text()
            
            # 余分な空行を削除
            text = re.sub(r'\n{3,}', '\n\n', text)
            
            f.write(text.strip())
        
        print(f"  保存完了: {filename}")
        return True
        
    except Exception as e:
        print(f"  エラー: {e}")
        return False

def main():
    """メイン処理"""
    # 出力ディレクトリ
    output_dir = Path(__file__).parent / "articles"
    output_dir.mkdir(exist_ok=True)
    
    print("壁の道の向こう側の記事スクレイピング開始")
    print(f"出力先: {output_dir}")
    print(f"記事数: {len(ARTICLES)}件\n")
    
    success_count = 0
    fail_count = 0
    
    for i, article in enumerate(ARTICLES, 1):
        print(f"\n[{i}/{len(ARTICLES)}]")
        
        if scrape_article(article['url'], article['title'], article['date'], output_dir):
            success_count += 1
        else:
            fail_count += 1
        
        # サーバーへの負荷を考慮して待機
        if i < len(ARTICLES):
            time.sleep(2)
    
    print(f"\n\n=== 完了 ===")
    print(f"成功: {success_count}件")
    print(f"失敗: {fail_count}件")

if __name__ == "__main__":
    main()
