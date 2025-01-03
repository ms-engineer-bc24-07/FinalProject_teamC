import os
from firebase_admin import credentials, initialize_app, auth
from dotenv import load_dotenv

# .env ファイルを読み込む
load_dotenv()

# 環境変数からファイルパスを取得
firebase_credentials_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "./firebase_credentials.json")

# 環境変数が設定されていない場合はエラー
if not firebase_credentials_path:
    raise ValueError("環境変数 'FIREBASE_CREDENTIALS_PATH' が設定されていません。")

print(f"Firebase credentials path: {firebase_credentials_path}")

# Firebase Admin SDK の初期化
cred = credentials.Certificate(firebase_credentials_path)
firebase_app = initialize_app(cred)

# 初期化成功メッセージの確認
try:
    print("Firebase Admin SDK 初期化成功")
except Exception as e:
    print("エラーが発生しました:", e)

# Firebaseトークン検証を行う関数（サーバーのリクエストで利用）
def verify_firebase_token(id_token):
    """
    Firebase IDトークンを検証する関数
    :param id_token: クライアントから送られるFirebaseのIDトークン
    :return: 検証されたトークン情報、またはエラーをスロー
    """
    try:
        decoded_token = auth.verify_id_token(id_token)
        print("トークンが正常に検証されました:", decoded_token)
        return decoded_token
    except auth.ExpiredIdTokenError:
        print("トークンが期限切れです")
        raise ValueError("トークンが期限切れです")
    except auth.InvalidIdTokenError:
        print("トークンが無効です")
        raise ValueError("トークンが無効です")
    except Exception as e:
        print("トークン検証中にエラーが発生しました:", e)
        raise
