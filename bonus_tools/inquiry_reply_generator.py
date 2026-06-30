#!/usr/bin/env python3
"""
購入特典ツール: 問い合わせ返信ジェネレーター

AI・フリーランス向けに、顧客属性と問い合わせ内容から
冷たくならない返信文を即座に生成する。
APIキー不要（テンプレートベース）。OpenAI API があれば拡張可能。
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

TEMPLATES: dict[str, dict[str, str]] = {
    "新規問い合わせ": {
        "丁寧": (
            "お問い合わせいただきありがとうございます。\n"
            "{sender}と申します。\n\n"
            "ご連絡いただいた「{topic}」について、内容を確認いたしました。\n"
            "詳細をお伺いしたうえで、{deadline}までにご返答いたします。\n\n"
            "差し支えなければ、{question}を教えていただけますでしょうか。\n"
            "お忙しいところ恐れ入りますが、何卒よろしくお願いいたします。"
        ),
        "カジュアル": (
            "お問い合わせありがとうございます！{sender}です。\n\n"
            "「{topic}」の件、拝見しました。\n"
            "{deadline}までに回答しますね。\n\n"
            "もし差し支えなければ、{question}を教えてください。\n"
            "よろしくお願いします！"
        ),
    },
    "料金・見積もり": {
        "丁寧": (
            "お見積もりのご依頼、誠にありがとうございます。\n\n"
            "「{topic}」について、以下の内容で進めさせていただきます。\n"
            "・対応範囲: {scope}\n"
            "・納期目安: {deadline}\n"
            "・概算費用: {price}\n\n"
            "詳細はヒアリング後に正式なお見積もりをお送りします。\n"
            "ご不明点があればお気軽にお知らせください。"
        ),
        "カジュアル": (
            "見積もりのご連絡ありがとうございます！\n\n"
            "「{topic}」の件、ざっくり以下のイメージです。\n"
            "・内容: {scope}\n"
            "・目安納期: {deadline}\n"
            "・概算: {price}\n\n"
            "詳しくお話しできれば、より正確な金額をお伝えできます。\n"
            "ご検討よろしくお願いします！"
        ),
    },
    "クレーム・トラブル": {
        "丁寧": (
            "この度はご不便をおかけし、誠に申し訳ございません。\n\n"
            "「{topic}」の件、状況を把握いたしました。\n"
            "まずは{action}を進めております。\n\n"
            "{deadline}までに改めてご連絡いたします。\n"
            "お急ぎの場合はその旨お知らせください。\n"
            "貴重なご意見をいただき、ありがとうございます。"
        ),
        "カジュアル": (
            "ご連絡ありがとうございます。ご不便をおかけしてすみません。\n\n"
            "「{topic}」の件、確認しました。\n"
            "今、{action}を進めています。\n\n"
            "{deadline}までにまたご連絡します。\n"
            "お急ぎであれば教えてください！"
        ),
    },
    "納期・進捗確認": {
        "丁寧": (
            "進捗のご確認、ありがとうございます。\n\n"
            "現在の状況をご報告します。\n"
            "・進捗: {scope}\n"
            "・次のステップ: {action}\n"
            "・完了予定: {deadline}\n\n"
            "ご不明点があればいつでもお知らせください。"
        ),
        "カジュアル": (
            "進捗確認ありがとうございます！\n\n"
            "今の状況です。\n"
            "・進捗: {scope}\n"
            "・次: {action}\n"
            "・完了予定: {deadline}\n\n"
            "気になることがあればいつでもどうぞ！"
        ),
    },
}

DEFAULTS = {
    "sender": "担当者",
    "topic": "（問い合わせ内容をここに入力）",
    "deadline": "24時間以内",
    "question": "ご希望の納期や予算感",
    "scope": "ヒアリング後に確定",
    "price": "ヒアリング後にお見積もり",
    "action": "原因の調査と対応策の検討",
}


def generate_reply(
    inquiry_type: str,
    tone: str = "丁寧",
    **fields: str,
) -> str:
    """返信文を生成する。"""
    if inquiry_type not in TEMPLATES:
        available = ", ".join(TEMPLATES.keys())
        raise ValueError(f"不明な問い合わせ種別: {inquiry_type}（選択肢: {available}）")

    if tone not in TEMPLATES[inquiry_type]:
        tone = next(iter(TEMPLATES[inquiry_type]))

    merged = {**DEFAULTS, **fields}
    template = TEMPLATES[inquiry_type][tone]
    return template.format(**merged)


def interactive_mode() -> str:
    """対話形式で返信文を生成する。"""
    print("\n=== 問い合わせ返信ジェネレーター（Nfcchipplatform 特典ツール）===\n")
    print("問い合わせ種別:")
    types = list(TEMPLATES.keys())
    for i, t in enumerate(types, 1):
        print(f"  {i}. {t}")
    choice = input("\n番号を選択 [1]: ").strip() or "1"
    idx = int(choice) - 1 if choice.isdigit() else 0
    inquiry_type = types[max(0, min(idx, len(types) - 1))]

    tone = input("トーン (丁寧/カジュアル) [丁寧]: ").strip() or "丁寧"
    topic = input("問い合わせ内容の要約: ").strip() or DEFAULTS["topic"]
    sender = input("あなたの名前・屋号 [担当者]: ").strip() or DEFAULTS["sender"]

    reply = generate_reply(
        inquiry_type,
        tone=tone,
        topic=topic,
        sender=sender,
    )
    return reply


def main() -> int:
    parser = argparse.ArgumentParser(description="問い合わせ返信ジェネレーター（購入特典ツール）")
    parser.add_argument("--type", choices=list(TEMPLATES.keys()), help="問い合わせ種別")
    parser.add_argument("--tone", choices=["丁寧", "カジュアル"], default="丁寧")
    parser.add_argument("--topic", default="", help="問い合わせ内容の要約")
    parser.add_argument("--sender", default="担当者", help="署名")
    parser.add_argument("--output", "-o", help="出力ファイルパス")
    parser.add_argument("--interactive", "-i", action="store_true", help="対話モード")
    args = parser.parse_args()

    if args.interactive or not args.type:
        reply = interactive_mode()
    else:
        reply = generate_reply(
            args.type,
            tone=args.tone,
            topic=args.topic or DEFAULTS["topic"],
            sender=args.sender,
        )

    print("\n" + "─" * 40)
    print("【生成された返信文】")
    print("─" * 40)
    print(reply)
    print("─" * 40)

    if args.output:
        out = Path(args.output)
        out.write_text(reply, encoding="utf-8")
        print(f"\n保存しました: {out}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
