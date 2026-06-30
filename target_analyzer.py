"""記事ターゲット分析・スコアリングモジュール"""

from __future__ import annotations

from typing import Any

# ホットキーワード（記事のトレンド性・関連性）
HOT_KEYWORDS: dict[str, int] = {
    "自動化": 15,
    "AI": 12,
    "ChatGPT": 10,
    "SNS": 10,
    "X": 8,
    "Twitter": 8,
    "運用": 10,
    "稼ぐ": 12,
    "副業": 10,
    "ツール": 12,
    "量産": 10,
    "GAS": 8,
    "Python": 8,
}

# 手作業・定型作業を示唆するキーワード（特典ツール化しやすさ）
MANUAL_WORK_KEYWORDS: dict[str, int] = {
    "手作業": 20,
    "コピペ": 18,
    "テンプレート": 12,
    "投稿": 10,
    "収集": 12,
    "まとめ": 10,
    "入力": 12,
    "転記": 15,
    "チェックリスト": 10,
    "定型": 10,
    "繰り返し": 10,
    "毎回": 8,
    "手順": 8,
    "データ": 8,
    "スプレッドシート": 10,
    "Excel": 8,
    "Notion": 8,
}


def _score_title(title: str) -> int:
    """タイトルに基づいてスコアを算出する。"""
    score = 0
    title_upper = title.upper()

    for keyword, weight in HOT_KEYWORDS.items():
        if keyword.upper() in title_upper or keyword in title:
            score += weight

    for keyword, weight in MANUAL_WORK_KEYWORDS.items():
        if keyword in title:
            score += weight

    return score


def _engagement_bonus(article: dict[str, Any]) -> int:
    """いいね数に基づくボーナススコア。"""
    likes = article.get("likes", 0)
    if isinstance(likes, int) and likes > 0:
        return min(likes // 10, 20)
    return 0


def score_articles(articles: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """全記事にスコアを付与し、スコア降順で返す。"""
    scored: list[dict[str, Any]] = []

    for article in articles:
        title = article.get("title", "")
        title_score = _score_title(title)
        bonus = _engagement_bonus(article)
        total_score = title_score + bonus

        scored.append(
            {
                **article,
                "score": total_score,
                "title_score": title_score,
                "engagement_bonus": bonus,
            }
        )

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored


def select_top_target(articles: list[dict[str, Any]]) -> dict[str, Any] | None:
    """
    記事群から最も特典ツール化しやすい Top 1 を選定する。

    Returns:
        スコア付きの最適ターゲット記事。入力が空の場合は None。
    """
    if not articles:
        return None

    scored = score_articles(articles)
    return scored[0]
