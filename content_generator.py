"""Tips 販売記事・X 投稿文の自動生成"""

from __future__ import annotations

from datetime import datetime, timezone


def generate_tips_article(
    target_title: str,
    bonus_idea: str,
    affiliate_account: str = "Nfcchipplatform",
) -> str:
    """Tips にそのまま投稿できる記事下書きを生成する。"""
    return f"""# 【購入特典付】AI問い合わせ返信を10秒で作る実践キット

> ライター: {affiliate_account}
> カテゴリ: AIテクノロジー / ビジネス
> 推奨価格: ¥1,480〜¥1,980

---

## こんな人向け

- AIに返信を書かせたいが、冷たい文章になってしまう
- 毎回同じような問い合わせに時間を取られている
- フリーランス・ひとり社長で顧客対応を効率化したい

## この記事で得られること

1. 冷たくならない返信の型（4パターン）
2. 問い合わせ種別ごとの最適なトーン設計
3. **購入特典: Python 返信ジェネレーター**（コピペですぐ使える）

## なぜ今これが必要か

トレンド記事「{target_title}」でも注目されている通り、
AIを使った問い合わせ対応の需要が急増しています。

しかし多くの人が「AIに丸投げ → 冷たい返信 → 顧客離れ」で失敗します。

本記事では、**AIの効率さと人間味のある対応**を両立する方法を解説します。

---

## 第1章: 冷たい返信になる3つの原因

1. テンプレートが「ビジネス文書」すぎる
2. 相手の状況を無視している
3. 次のアクションが不明確

## 第2章: 4つの問い合わせパターンと最適な返信設計

| パターン | トーン | 必須要素 |
|---|---|---|
| 新規問い合わせ | 丁寧＋期待感 | 感謝・確認・次の質問 |
| 料金・見積もり | 明確＋柔らかさ | 範囲・納期・概算 |
| クレーム | 謝罪＋具体行動 | 共感・対応策・期限 |
| 進捗確認 | 簡潔＋安心感 | 現状・次ステップ・完了日 |

## 第3章: AIとの正しい使い分け

- AIに「下書き」まで任せる
- 人間が「温度」を調整する
- 特典ツールで一発生成 → 微調整で完了

---

## 🎁 購入特典

{bonus_idea}

**同梱ファイル:**
- `inquiry_reply_generator.py` — 対話形式で返信文を即生成
- 使い方: `python inquiry_reply_generator.py -i`

---

## まとめ

問い合わせ対応は「速さ」と「人間味」の両立がカギ。
この記事＋特典ツールで、1件あたりの対応時間を5分→30秒に短縮できます。

---

*アフィリエイト報酬率: 30%推奨（紹介してくれた人にもメリットを）*
"""


def generate_x_posts(
    article_title: str,
    tips_url: str = "（公開後に自分のTips記事URLを入れる）",
    affiliate_account: str = "Nfcchipplatform",
) -> list[dict[str, str]]:
    """X（Twitter）投稿文を複数パターン生成する。"""
    posts = [
        {
            "purpose": "自分の記事を売る（初回告知）",
            "text": (
                f"AIに問い合わせ返信を書かせると、冷たい文章になりがちですよね。\n\n"
                f"そこで「人間味のある返信を10秒で作る」キットを作りました。\n"
                f"購入特典にPythonツール付き。\n\n"
                f"詳細はこちら👇\n"
                f"{tips_url}\n\n"
                f"#{affiliate_account} #AI活用 #フリーランス #業務効率化"
            ),
        },
        {
            "purpose": "悩み共感型（売上狙い）",
            "text": (
                f"毎回同じ問い合わせに30分使ってませんか？\n\n"
                f"僕は返信テンプレ＋Pythonツールで\n"
                f"対応時間を30秒に短縮しました。\n\n"
                f"ノウハウ全部まとめた👇\n"
                f"{tips_url}\n\n"
                f"#ひとり社長 #業務効率化 #Tips"
            ),
        },
        {
            "purpose": "他者記事のアフィリエイト紹介（#ad必須）",
            "text": (
                f"「{article_title}」\n"
                f"を実践してみた感想。\n\n"
                f"✅ テンプレの型がそのまま使える\n"
                f"✅ AIとの使い分けが明確\n"
                f"⚠️ ツールは自作が必要（僕は特典ツール作った）\n\n"
                f"気になる人はこちら👇\n"
                f"（購入済みならアフィリエイトリンクを貼る）\n\n"
                f"#ad #PR #AI活用 #Tips"
            ),
        },
        {
            "purpose": "実績報告型（信頼構築→売上）",
            "text": (
                f"Tipsアフィリエイト始めてみた。\n\n"
                f"まずは自分が使えるツールを作って\n"
                f"記事にした。これが一番大事だと思う。\n\n"
                f"作った特典ツール: 問い合わせ返信ジェネレーター\n"
                f"記事はこちら👇\n"
                f"{tips_url}\n\n"
                f"#{affiliate_account} #副業 #Tips"
            ),
        },
    ]
    return posts


def generate_action_checklist(affiliate_account: str = "Nfcchipplatform") -> list[str]:
    """今日から稼ぐための行動チェックリスト。"""
    return [
        f"[ ] Tips にログイン（アカウント: {affiliate_account}）",
        "[ ] アフィリエイター登録（https://tips.jp/affiliate）",
        "[ ] 記事下書きを Tips に投稿（価格 ¥1,480〜¥1,980 推奨）",
        "[ ] 購入特典に bonus_tools/inquiry_reply_generator.py を同梱",
        "[ ] アフィリエイト報酬率を 30% に設定（紹介者を増やす）",
        "[ ] X に投稿文をコピペして投稿（#ad はアフィリエイト時必須）",
        "[ ] 自分が購入した他記事があれば、アフィリエイトリンクで紹介投稿",
        "[ ] 週1回: python earn_campaign.py でトレンド確認 → 新記事 or 投稿更新",
    ]
