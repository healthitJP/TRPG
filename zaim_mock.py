import os
from requests_oauthlib import OAuth1Session
import json

# 認証情報
CONSUMER_KEY = "470e09548a79a7f6f46772bd5a3d6dd81f64af85"
CONSUMER_SECRET = "9444e570c9d5505eef8de886ab3bc93902973234"
CALLBACK_URL = "https://n8n.ushida-yosei.jp/rest/oauth1-credential/callback"

# APIのエンドポイント
REQUEST_TOKEN_URL = "https://api.zaim.net/v2/auth/request"
AUTHORIZE_URL = "https://auth.zaim.net/users/auth"
ACCESS_TOKEN_URL = "https://api.zaim.net/v2/auth/access"
API_BASE = "https://api.zaim.net/v2"

class ZaimAPI:
    def __init__(self):
        self.oauth = None
        self.request_token = None
        self.request_token_secret = None
        self.access_token = None
        self.access_token_secret = None

    def get_request_token(self):
        """リクエストトークンを取得"""
        oauth = OAuth1Session(
            CONSUMER_KEY,
            client_secret=CONSUMER_SECRET,
            callback_uri=CALLBACK_URL
        )
        
        try:
            fetch_response = oauth.fetch_request_token(REQUEST_TOKEN_URL)
            self.request_token = fetch_response.get('oauth_token')
            self.request_token_secret = fetch_response.get('oauth_token_secret')
            
            # 認証URLを生成
            authorize_url = f"{AUTHORIZE_URL}?oauth_token={self.request_token}"
            print(f"以下のURLにアクセスして認証してください：\n{authorize_url}")
            
            return authorize_url
            
        except Exception as e:
            print(f"リクエストトークンの取得に失敗しました: {e}")
            return None

    def get_access_token(self, oauth_verifier):
        """アクセストークンを取得"""
        if not self.request_token or not self.request_token_secret:
            print("リクエストトークンが存在しません。先にget_request_tokenを実行してください。")
            return False

        oauth = OAuth1Session(
            CONSUMER_KEY,
            client_secret=CONSUMER_SECRET,
            resource_owner_key=self.request_token,
            resource_owner_secret=self.request_token_secret,
            verifier=oauth_verifier
        )

        try:
            oauth_tokens = oauth.fetch_access_token(ACCESS_TOKEN_URL)
            self.access_token = oauth_tokens.get('oauth_token')
            self.access_token_secret = oauth_tokens.get('oauth_token_secret')
            
            # 認証済みのセッションを作成
            self.oauth = OAuth1Session(
                CONSUMER_KEY,
                client_secret=CONSUMER_SECRET,
                resource_owner_key=self.access_token,
                resource_owner_secret=self.access_token_secret
            )
            
            return True
            
        except Exception as e:
            print(f"アクセストークンの取得に失敗しました: {e}")
            return False

    def verify_user(self):
        """ユーザー情報を取得"""
        if not self.oauth:
            print("認証が完了していません。")
            return None

        try:
            response = self.oauth.get(f"{API_BASE}/home/user/verify")
            return response.json()
        except Exception as e:
            print(f"ユーザー情報の取得に失敗しました: {e}")
            return None

    def get_money(self, **params):
        """入出金履歴を取得"""
        if not self.oauth:
            print("認証が完了していません。")
            return None

        try:
            params['mapping'] = 1  # 必須パラメータ
            response = self.oauth.get(f"{API_BASE}/home/money", params=params)
            return response.json()
        except Exception as e:
            print(f"入出金履歴の取得に失敗しました: {e}")
            return None

# 使用例
if __name__ == "__main__":
    zaim = ZaimAPI()
    
    # Step 1: リクエストトークンを取得して認証URLを表示
    auth_url = zaim.get_request_token()
    if not auth_url:
        print("認証URLの取得に失敗しました。")
        exit(1)
    
    # Step 2: ユーザーに認証後のverifierの入力を求める
    print("\n認証が完了したら、表示されたverifierを入力してください：")
    oauth_verifier = input("Verifier: ")
    
    # Step 3: アクセストークンを取得
    if not zaim.get_access_token(oauth_verifier):
        print("アクセストークンの取得に失敗しました。")
        exit(1)
    
    # Step 4: ユーザー情報を取得してみる
    user_info = zaim.verify_user()
    if user_info:
        print("\nユーザー情報:")
        print(json.dumps(user_info, indent=2, ensure_ascii=False))
    
    # Step 5: 入出金履歴を取得してみる
    money_info = zaim.get_money(limit=5)  # 最新5件を取得
    if money_info:
        print("\n入出金履歴:")
        print(json.dumps(money_info, indent=2, ensure_ascii=False)) 