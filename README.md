# Tips Affiliate Automator

Tips.jp のアフィリエイト向けに、トレンド記事のリサーチから購入特典ツールのアイデア出しまでを自動化する Python システムです。

## セットアップ

```bash
pip install -r requirements.txt
```

## 使い方

```bash
# 通常実行（Tips.jp から記事を取得して分析）
python main_automator.py

# モックデータで動作確認
python main_automator.py --mock

# キーワードを指定
python main_automator.py --keywords AI X運用 副業

# 結果を JSON に保存
python main_automator.py --output report.json
```

## ファイル構成

| ファイル | 説明 |
|---|---|
| `tips_scraper.py` | Tips.jp 検索結果のスクレイピング（失敗時はモックにフォールバック） |
| `target_analyzer.py` | 記事のスコアリングと Top 1 選定 |
| `idea_generator.py` | 特典ツールアイデアの自動生成 |
| `main_automator.py` | Rich CUI による統合実行スクリプト |

## アカウント

Nfcchipplatform 向けに構築されています。
