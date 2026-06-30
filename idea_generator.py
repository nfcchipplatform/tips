"""購入特典ツールアイデア生成モジュール"""

from __future__ import annotations


def generate_bonus_idea(title: str) -> str:
    """
    記事タイトルから、Nfcchipplatform が開発すべき特典ツールのアイデアを生成する。

    Args:
        title: ターゲット記事のタイトル

    Returns:
        特典ツールのアイデア文
    """
    title_lower = title.lower()

    # X / Twitter 系
    if any(kw in title for kw in ("X", "Twitter", "ツイート", "ポスト")) or "x運用" in title_lower:
        return (
            "特典アイデア: 特定キーワードのポストを自動収集し、"
            "スプレッドシートにまとめる Python スクリプト"
        )

    # ブログ / 記事系
    if any(kw in title for kw in ("ブログ", "記事", "note", "SEO", "コンテンツ")):
        return (
            "特典アイデア: SEOキーワードから見出し構成を自動生成する"
            "プロンプト＆スクリプト"
        )

    # テンプレート / メール / 返信系
    if any(kw in title for kw in ("テンプレート", "返信", "メール", "問い合わせ")):
        return (
            "特典アイデア: 顧客属性に応じた返信文をワンクリック生成する"
            "Python + ChatGPT API 連携ツール"
        )

    # データ入出力 / GAS系
    if any(kw in title for kw in ("GAS", "スプレッドシート", "Excel", "データ", "入力")):
        return (
            "特典アイデア: CSV/スプレッドシートへの一括データ入出力を"
            "自動化する GAS スクリプト＋操作マニュアル"
        )

    # チェックリスト / 公開前確認系
    if any(kw in title for kw in ("チェックリスト", "公開前", "確認", "チェック")):
        return (
            "特典アイデア: 記事公開前の品質チェックを自動実行する"
            "Python チェックリストツール（PDFレポート出力付き）"
        )

    # デフォルト
    return (
        "特典アイデア: 記事内のノウハウを対話形式で実行できる"
        "専用チャットボットスクリプト"
    )
