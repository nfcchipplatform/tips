#!/usr/bin/env python3
"""Tips アフィリエイト自動リサーチ＆特典アイデア生成メインスクリプト"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from idea_generator import generate_bonus_idea
from target_analyzer import score_articles, select_top_target
from tips_scraper import DEFAULT_SEARCH_KEYWORDS, fetch_trending_articles

console = Console()
AFFILIATE_ACCOUNT = "Nfcchipplatform"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Tips.jp アフィリエイト向け 記事リサーチ＆特典ツールアイデア自動生成",
    )
    parser.add_argument(
        "--keywords",
        nargs="+",
        metavar="KW",
        help=f"検索キーワード（デフォルト: {' '.join(DEFAULT_SEARCH_KEYWORDS)}）",
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="スクレイピングをスキップし、モックデータで動作確認する",
    )
    parser.add_argument(
        "--output",
        "-o",
        metavar="FILE",
        help="分析結果を JSON ファイルに保存する（例: report.json）",
    )
    return parser.parse_args()


def _print_banner() -> None:
    banner = Text()
    banner.append("╔══════════════════════════════════════════════════════════╗\n", style="bold cyan")
    banner.append("║  ", style="bold cyan")
    banner.append("Tips Affiliate Automator", style="bold white on blue")
    banner.append("  —  Nfcchipplatform Edition  ║\n", style="bold cyan")
    banner.append("╚══════════════════════════════════════════════════════════╝", style="bold cyan")
    console.print(banner)
    console.print()


def _display_articles_table(articles: list[dict]) -> None:
    table = Table(
        title="[bold green]📋 取得記事一覧[/bold green]",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold magenta",
        border_style="bright_blue",
    )
    table.add_column("#", style="dim", width=4, justify="right")
    table.add_column("タイトル", style="white", max_width=50, overflow="fold")
    table.add_column("価格", style="yellow", width=12)
    table.add_column("いいね", style="red", width=8, justify="right")
    table.add_column("KW", style="cyan", width=8)

    for idx, article in enumerate(articles, start=1):
        table.add_row(
            str(idx),
            article.get("title", "—"),
            article.get("price", "—"),
            str(article.get("likes", 0)),
            article.get("keyword", "—"),
        )

    console.print(table)
    console.print()


def _display_scored_table(scored: list[dict], top_n: int = 5) -> None:
    table = Table(
        title=f"[bold yellow]🎯 スコアリング Top {min(top_n, len(scored))}[/bold yellow]",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold magenta",
        border_style="bright_yellow",
    )
    table.add_column("順位", width=6, justify="center")
    table.add_column("スコア", width=8, justify="right", style="bold green")
    table.add_column("タイトル", max_width=45, overflow="fold")

    for rank, article in enumerate(scored[:top_n], start=1):
        table.add_row(
            f"#{rank}",
            str(article.get("score", 0)),
            article.get("title", "—"),
        )

    console.print(table)
    console.print()


def _display_final_result(target: dict, idea: str) -> None:
    result_text = Text()
    result_text.append("【ターゲット記事】\n\n", style="bold white")
    result_text.append("  タイトル: ", style="dim")
    result_text.append(f"{target['title']}\n\n", style="bold bright_white")
    result_text.append("  URL:      ", style="dim")
    result_text.append(f"{target['url']}\n\n", style="underline bright_cyan")
    result_text.append("  スコア:   ", style="dim")
    result_text.append(f"{target.get('score', 0)} pt\n\n", style="bold green")
    result_text.append("─" * 50 + "\n\n", style="dim")
    result_text.append(f"【{AFFILIATE_ACCOUNT} が開発すべき特典ツール】\n\n", style="bold white")
    result_text.append(f"  💡 {idea}\n", style="bold bright_yellow")

    console.print(
        Panel(
            result_text,
            title="[bold red]★ FINAL TARGET ★[/bold red]",
            border_style="bright_red",
            padding=(1, 2),
            box=box.DOUBLE_EDGE,
        )
    )


def _save_report(
    output_path: str,
    keywords: list[str],
    articles: list[dict],
    scored: list[dict],
    target: dict,
    idea: str,
) -> None:
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "affiliate_account": AFFILIATE_ACCOUNT,
        "search_keywords": keywords,
        "article_count": len(articles),
        "articles": articles,
        "scored_articles": scored,
        "top_target": target,
        "bonus_tool_idea": idea,
    }

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    console.print(f"[bold green]✓[/bold green] レポートを保存しました: [cyan]{path}[/cyan]\n")


def run(args: argparse.Namespace | None = None) -> int:
    """メイン実行フロー。"""
    if args is None:
        args = _parse_args()

    keywords = args.keywords or DEFAULT_SEARCH_KEYWORDS
    _print_banner()

    if args.mock:
        console.print("[dim]※ モックモードで実行中（--mock）[/dim]\n")

    keywords_str = ", ".join(keywords)
    with console.status(
        f"[bold cyan]Tips から最新の AI/副業系トレンド記事を抽出中...[/bold cyan] "
        f"[dim]({keywords_str})[/dim]",
        spinner="dots",
    ):
        articles = fetch_trending_articles(
            keywords=keywords,
            force_mock=args.mock,
        )

    console.print(
        f"[bold green]✓[/bold green] {len(articles)} 件の記事を取得しました。\n"
    )
    _display_articles_table(articles)

    with console.status(
        "[bold yellow]最適なターゲットを分析中...[/bold yellow]",
        spinner="line",
    ):
        scored = score_articles(articles)
        target = select_top_target(articles)

    if not target:
        console.print("[bold red]エラー:[/bold red] 分析対象の記事がありません。")
        return 1

    _display_scored_table(scored)

    idea = generate_bonus_idea(target["title"])
    _display_final_result(target, idea)

    if args.output:
        _save_report(args.output, keywords, articles, scored, target, idea)

    console.print(
        f"\n[dim]{'─' * 50}[/dim]\n"
        f"[dim]Powered by {AFFILIATE_ACCOUNT} | Tips Affiliate Automator v1.0[/dim]\n"
    )
    return 0


if __name__ == "__main__":
    sys.exit(run())
