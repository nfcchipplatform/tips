#!/usr/bin/env python3
"""
Tips アフィリエイト稼ぎ用キャンペーン実行スクリプト

リサーチ → 特典ツール → Tips記事下書き → X投稿文 → 行動チェックリスト
を一括出力する。これが「稼ぐための」メインスクリプト。
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from content_generator import (
    generate_action_checklist,
    generate_tips_article,
    generate_x_posts,
)
from idea_generator import generate_bonus_idea
from target_analyzer import score_articles, select_top_target
from tips_scraper import DEFAULT_SEARCH_KEYWORDS, fetch_trending_articles

console = Console()
AFFILIATE_ACCOUNT = "Nfcchipplatform"
OUTPUT_DIR = Path("content")


def _save_campaign_files(
    target: dict,
    idea: str,
    article: str,
    posts: list[dict],
    checklist: list[str],
) -> Path:
    """キャンペーン成果物を content/ に保存する。"""
    OUTPUT_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d")

    article_path = OUTPUT_DIR / f"tips_article_{timestamp}.txt"
    article_path.write_text(article, encoding="utf-8")

    posts_path = OUTPUT_DIR / f"x_posts_{timestamp}.txt"
    posts_text = ""
    for i, post in enumerate(posts, 1):
        posts_text += f"--- 投稿{i}: {post['purpose']} ---\n\n"
        posts_text += post["text"] + "\n\n"
    posts_path.write_text(posts_text, encoding="utf-8")

    checklist_path = OUTPUT_DIR / f"action_checklist_{timestamp}.txt"
    checklist_path.write_text("\n".join(checklist), encoding="utf-8")

    summary_path = OUTPUT_DIR / f"campaign_summary_{timestamp}.txt"
    summary_path.write_text(
        f"ターゲット記事: {target['title']}\n"
        f"URL: {target['url']}\n"
        f"スコア: {target.get('score', 0)} pt\n\n"
        f"特典アイデア: {idea}\n\n"
        f"成果物:\n"
        f"  - {article_path}\n"
        f"  - {posts_path}\n"
        f"  - {checklist_path}\n"
        f"  - bonus_tools/inquiry_reply_generator.py\n",
        encoding="utf-8",
    )

    return summary_path


def run(args: argparse.Namespace) -> int:
    console.print()
    console.print(
        Panel(
            f"[bold white]Tips アフィリエイト稼ぎキャンペーン[/bold white]\n"
            f"[dim]アカウント: {AFFILIATE_ACCOUNT}[/dim]",
            border_style="green",
            box=box.DOUBLE,
        )
    )
    console.print()

    # Step 1: リサーチ
    with console.status("[cyan]Step 1/4[/cyan] トレンド記事をリサーチ中...", spinner="dots"):
        articles = fetch_trending_articles(
            keywords=args.keywords or DEFAULT_SEARCH_KEYWORDS,
            force_mock=args.mock,
        )
        scored = score_articles(articles)
        target = select_top_target(articles)

    if not target:
        console.print("[red]記事が取得できませんでした。[/red]")
        return 1

    idea = generate_bonus_idea(target["title"])

    console.print(f"[green]✓[/green] ターゲット: [bold]{target['title'][:50]}...[/bold]")
    console.print(f"[green]✓[/green] 特典アイデア: {idea}\n")

    # Step 2: 記事下書き
    with console.status("[cyan]Step 2/4[/cyan] Tips 販売記事の下書きを生成中...", spinner="line"):
        article = generate_tips_article(target["title"], idea, AFFILIATE_ACCOUNT)

    console.print("[green]✓[/green] Tips 記事下書きを生成しました\n")

    # Step 3: X 投稿文
    with console.status("[cyan]Step 3/4[/cyan] X 投稿文を生成中...", spinner="line"):
        posts = generate_x_posts(target["title"], tips_url=args.tips_url)

    console.print(f"[green]✓[/green] X 投稿文 {len(posts)} パターンを生成しました\n")

    # Step 4: 保存
    checklist = generate_action_checklist(AFFILIATE_ACCOUNT)
    summary_path = _save_campaign_files(target, idea, article, posts, checklist)

    console.print(f"[green]✓[/green] 成果物を保存しました: [cyan]{OUTPUT_DIR}/[/cyan]\n")

    # 行動チェックリスト表示
    table = Table(title="[bold yellow]今日やること（これで稼ぎ始める）[/bold yellow]", box=box.ROUNDED)
    table.add_column("No.", width=4, justify="right")
    table.add_column("アクション", style="white")

    for i, item in enumerate(checklist, 1):
        table.add_row(str(i), item.replace("[ ] ", ""))

    console.print(table)
    console.print()

    # X投稿プレビュー
    console.print(Panel(
        posts[0]["text"],
        title=f"[bold cyan]X投稿サンプル（{posts[0]['purpose']}）[/bold cyan]",
        border_style="cyan",
    ))

    console.print()
    console.print(
        Panel(
            f"[bold]次の一手:[/bold]\n\n"
            f"1. [cyan]{OUTPUT_DIR}/[/cyan] 内の記事下書きを Tips に投稿\n"
            f"2. 特典ツール [cyan]bonus_tools/inquiry_reply_generator.py[/cyan] を同梱\n"
            f"3. X 投稿文をコピペして投稿開始\n\n"
            f"[dim]詳細: {summary_path}[/dim]",
            title="[bold green]💰 稼ぎスタート手順[/bold green]",
            border_style="green",
        )
    )

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Tips アフィリエイト稼ぎキャンペーン")
    parser.add_argument("--mock", action="store_true", help="モックデータで実行")
    parser.add_argument("--keywords", nargs="+", help="検索キーワード")
    parser.add_argument(
        "--tips-url",
        default="（公開後に自分のTips記事URLを入れる）",
        help="自分の Tips 記事 URL（X投稿文に挿入）",
    )
    return run(parser.parse_args())


if __name__ == "__main__":
    sys.exit(main())
