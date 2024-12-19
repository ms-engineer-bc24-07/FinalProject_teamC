# backend/api/tests/api_test.py
# 外部API疎通確認

import os

import openai
import requests
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# Google Maps APIキー
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# HotPepper APIキー
HOTPEPPER_API_KEY = os.getenv("HOTPEPPER_API_KEY")

# OpenAI APIキー
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# Google Maps APIの疎通確認
def test_google_maps_api(station):
    try:
        response = requests.get(
            "https://maps.googleapis.com/maps/api/geocode/json",
            params={
                "address": f"{station}駅",
                "key": GOOGLE_MAPS_API_KEY,
            },
        )
        response.raise_for_status()
        data = response.json()

        if not data["results"]:
            print("座標が見つかりませんでした。")
            return None

        location = data["results"][0]["geometry"]["location"]
        print(f"{station}駅の座標: 緯度={location['lat']}, 経度={location['lng']}")
        return location
    except (requests.RequestException, ValueError) as e:
        print(f"エラー: {e}")


# HotPepper APIの疎通確認
def test_hotpepper_api(lat, lng, keyword="居酒屋"):
    try:
        api_url = "https://webservice.recruit.co.jp/hotpepper/gourmet/v1/"
        params = {
            "key": HOTPEPPER_API_KEY,
            "lat": lat,
            "lng": lng,
            "range": 3,  # 検索範囲（3km）
            "keyword": keyword,  # 検索キーワード
            "format": "json",  # レスポンス形式
        }

        response = requests.get(api_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data.get("results") or not data["results"].get("shop"):
            print("店舗情報が見つかりませんでした。")
            return None

        print("検索結果:")
        for shop in data["results"]["shop"]:
            print(f"店名: {shop['name']}, 住所: {shop['address']}")
        return data["results"]["shop"]
    except requests.exceptions.Timeout:
        print("HotPepper API リクエストがタイムアウトしました。")
    except requests.exceptions.RequestException as e:
        print(f"エラー: {e}")
    except ValueError as e:
        print(f"エラー: {e}")


# OpenAI APIの疎通確認
def test_openai_api(shop_descriptions):
    try:
        # システムメッセージを定義
        prompt = (
            "You are an assistant that recommends the best shops based on user input.\n\n"
            "以下のお店の中から、最もおすすめの3つを提案してください。\n\n"
            + "\n".join(f"{i + 1}. {desc}" for i, desc in enumerate(shop_descriptions))
            + "\n\n提案結果:"
        )

        # OpenAI API呼び出し（v1/chat/completionsエンドポイント）
        response = openai.chat.completions.create(
            model="gpt-4",  # または "gpt-3.5-turbo"
            messages=[
                {
                    "role": "system",
                    "content": "You are an assistant that recommends the best shops based on user input.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,
            temperature=0.7,
        )

        # レスポンスの検証
        if not response.choices or not response.choices[0].message.content.strip():
            print("OpenAI APIのレスポンスが不正です。")
            return None

        # 推薦結果を取得
        recommendations = response.choices[0].message.content.strip()
        print(f"OpenAI APIからのおすすめ: {recommendations}")
        return recommendations
    except Exception as e:
        # すべてのエラーを一括で捕捉
        print(f"エラーが発生しました: {e}")


# テスト実行
if __name__ == "__main__":
    print("Google Maps API疎通確認:")
    test_google_maps_api("新宿")  # 任意の駅名を指定

    print("\nHotPepper API疎通確認:")
    test_hotpepper_api(35.6895, 139.6917)  # 新宿の緯度経度を指定

    print("\nOpenAI API疎通確認:")
    test_openai_api(
        [
            "店名: 居酒屋A, ジャンル: 居酒屋, 住所: 東京都新宿区",
            "店名: 居酒屋B, ジャンル: 居酒屋, 住所: 東京都渋谷区",
            "店名: 居酒屋C, ジャンル: 居酒屋, 住所: 東京都池袋区",
        ]
    )
