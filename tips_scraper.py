"""Tips.jp 検索結果スクレイパー"""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

DEFAULT_SEARCH_KEYWORDS = ["AI", "X運用", "自動化", "副業"]
BASE_URL = "https://tips.jp/search"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
REQUEST_TIMEOUT = 15


def _get_mock_articles() -> list[dict[str, Any]]:
    """動的レンダリングや取得失敗時のフォールバック用モックデータ。"""
    return [
        {
            "title": "【完全自動化】X運用を1日30分で回すAI量産術",
            "url": "https://tips.jp/u/example/a/x-ai-automation",
            "price": "¥2,980",
            "likes": 128,
            "keyword": "X運用",
        },
        {
            "title": "ChatGPTで副業ブログ記事を月100本量産する手順",
            "url": "https://tips.jp/u/example/a/chatgpt-blog-sidejob",
            "price": "¥1,480",
            "likes": 95,
            "keyword": "副業",
        },
        {
            "title": "コピペ作業をゼロにする業務自動化ツール構築ガイド",
            "url": "https://tips.jp/u/example/a/copypaste-automation",
            "price": "¥3,480",
            "likes": 76,
            "keyword": "自動化",
        },
        {
            "title": "AI×SNS運用で月5万円稼ぐ初心者向けロードマップ",
            "url": "https://tips.jp/u/example/a/ai-sns-income",
            "price": "¥980",
            "likes": 210,
            "keyword": "AI",
        },
        {
            "title": "手作業のデータ入力作業をGASで一括処理する実践ノウハウ",
            "url": "https://tips.jp/u/example/a/gas-data-entry",
            "price": "¥1,980",
            "likes": 54,
            "keyword": "自動化",
        },
    ]


def _parse_article(article_tag: Any, keyword: str) -> dict[str, Any] | None:
    """article 要素から記事情報を抽出する。"""
    title_el = article_tag.find("h2", class_="list-title")
    link_el = article_tag.find("a", class_="stretched-link", href=True)

    if not title_el or not link_el:
        return None

    title = title_el.get_text(strip=True)
    url = link_el["href"]
    if url.startswith("/"):
        url = f"https://tips.jp{url}"

    price_el = article_tag.find(class_="price") or article_tag.find(class_="yen")
    price = price_el.get_text(" ", strip=True) if price_el else "不明"

    clap_el = (
        article_tag.find(class_="clap-count-total")
        or article_tag.find(class_="clap-count")
    )
    likes_text = clap_el.get_text(strip=True) if clap_el else "0"
    try:
        likes = int(re.sub(r"[^\d]", "", likes_text) or "0")
    except ValueError:
        likes = 0

    return {
        "title": title,
        "url": url,
        "price": price,
        "likes": likes,
        "keyword": keyword,
    }


def _scrape_search_page(keyword: str) -> list[dict[str, Any]]:
    """単一キーワードの検索結果ページをスクレイピングする。"""
    url = f"{BASE_URL}?q={quote(keyword)}"
    headers = {"User-Agent": USER_AGENT}

    response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    articles: list[dict[str, Any]] = []

    for article_tag in soup.find_all("article"):
        parsed = _parse_article(article_tag, keyword)
        if parsed:
            articles.append(parsed)

    return articles


def _deduplicate_articles(articles: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """URL をキーに重複記事を除去する。"""
    seen: set[str] = set()
    unique: list[dict[str, Any]] = []

    for article in articles:
        url = article["url"]
        if url not in seen:
            seen.add(url)
            unique.append(article)

    return unique


def fetch_trending_articles(
    keywords: list[str] | None = None,
    use_mock_on_failure: bool = True,
    force_mock: bool = False,
) -> list[dict[str, Any]]:
    """
    Tips.jp からキーワード検索結果を取得し、記事リストを返す。

    取得に失敗した場合、または結果が空の場合はモックデータにフォールバックする。
    force_mock=True の場合はスクレイピングを行わずモックデータを返す。
    """
    if force_mock:
        return _get_mock_articles()

    search_keywords = keywords or DEFAULT_SEARCH_KEYWORDS
    all_articles: list[dict[str, Any]] = []

    for keyword in search_keywords:
        try:
            articles = _scrape_search_page(keyword)
            all_articles.extend(articles)
        except (requests.RequestException, ValueError):
            continue

    all_articles = _deduplicate_articles(all_articles)

    if all_articles:
        return all_articles

    if use_mock_on_failure:
        return _get_mock_articles()

    return []
