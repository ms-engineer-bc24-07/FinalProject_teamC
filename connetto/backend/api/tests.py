# from django.test import TestCase

# Create your tests here.
import os

from dotenv import load_dotenv

# .envファイルの読み込み
load_dotenv()

# 環境変数の確認
firebase_credentials_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
print(f"FIREBASE_CREDENTIALS_PATH: {firebase_credentials_path}")
print("Firebase Admin SDK 初期化成功")
