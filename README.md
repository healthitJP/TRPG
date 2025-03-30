# Zaim API モック

このプロジェクトは、Zaim APIのモック実装です。OAuth 1.0aを使用して認証を行い、Zaimの家計簿データにアクセスすることができます。

## セットアップ

1. 必要なパッケージをインストール:
```bash
pip install -r requirements.txt
```

2. 認証情報の確認:
以下の情報が`zaim_mock.py`に設定されていることを確認してください：
- CONSUMER_KEY
- CONSUMER_SECRET
- CALLBACK_URL

## 使い方

1. スクリプトを実行:
```bash
python zaim_mock.py
```

2. 表示されたURLにアクセスして認証を行います。

3. 認証後に表示されるverifierコードをコンソールに入力します。

4. 認証が成功すると、ユーザー情報と最新の入出金履歴（5件）が表示されます。

## 実装されている機能

- OAuth 1.0a認証
- ユーザー情報の取得
- 入出金履歴の取得

## 注意事項

- このモックはテスト用です。本番環境での使用は避けてください。
- APIキーは公開しないように注意してください。
- 認証情報は適切に管理してください。 