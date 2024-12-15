import firebase_admin
from firebase_admin import credentials, auth
import os
import logging
from pathlib import Path

# Firebaseの初期化
firebase_credentials_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
if not firebase_credentials_path:
    raise ValueError("FIREBASE_CREDENTIALS_PATH が設定されていません。")

firebase_credentials_path = Path(__file__).resolve().parent.parent / firebase_credentials_path

# Firebase Admin SDKの初期化
try:
    # すでに初期化されている場合は、get_app() で取得
    firebase_admin.get_app()
    logging.info("Firebaseはすでに初期化されています。")
except firebase_admin.exceptions.AppNotFoundError:
    # 初期化されていない場合は、ここで初期化する
    try:
        cred = credentials.Certificate(firebase_credentials_path)
        firebase_admin.initialize_app(cred)
        logging.info("Firebaseの初期化が完了しました。")
    except Exception as e:
        logging.error(f"Firebaseの初期化中にエラーが発生しました: {e}")

# Firebaseトークン検証用の関数
def verify_firebase_token(id_token):
    try:
        # トークンを検証してデコードする
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except auth.InvalidIdTokenError as e:
        # 無効なトークンエラーをより明確に
        raise ValueError("無効なトークンです") from e
    except Exception as e:
        # その他のエラー
        raise ValueError("トークン検証に失敗しました") from e
