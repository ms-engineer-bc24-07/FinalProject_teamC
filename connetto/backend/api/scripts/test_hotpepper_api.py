import requests
import os
from dotenv import load_dotenv
import logging

# 環境変数の読み込み
load_dotenv()

# ログの設定
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# APIキーの取得
HOTPEPPER_API_KEY = os.getenv("HOTPEPPER_API_KEY")  # .env にAPIキーを保存している場合

def get_restaurant_suggestions(lat, lng, range=3):
    """
    ホットペッパーAPIを使ってお店情報を取得する関数。
    
    Args:
        lat (float): 緯度
        lng (float): 経度
        range (int): 検索範囲（1: 300m, 2: 500m, 3: 1km, 4: 2km, 5: 3km）
    
    Returns:
        list: お店情報のリスト
    """
    try:
        # APIリクエストURL
        url = "https://webservice.recruit.co.jp/hotpepper/gourmet/v1/"
        
        # リクエストパラメータ
        params = {
            "key": HOTPEPPER_API_KEY,
            "lat": lat,
            "lng": lng,
            "range": range,
            "format": "json",
            "count": 3,  
        }

        logging.info(f"リクエストを送信: {url} パラメータ: {params}")

        # APIリクエスト送信
        response = requests.get(url, params=params)
        response.raise_for_status()  

        data = response.json()

        results = data.get("results", {})
        shops = results.get("shop", [])
        suggestions = [
            {
                "name": shop.get("name"),
                "url": shop.get("urls", {}).get("pc"),
                "address": shop.get("address"),
                "genre": shop.get("genre", {}).get("name"),
            }
            for shop in shops
        ]

        logging.info(f"取得したお店情報: {suggestions}")
        return suggestions

    except requests.exceptions.RequestException as e:
        logging.error(f"APIリクエストエラー: {e}")
        return []
    except Exception as e:
        logging.error(f"その他のエラー: {e}")
        return []

if __name__ == "__main__":
    # テスト用の緯度・経度（例: 川崎駅）
    latitude = 35.530753
    longitude = 139.703422

    restaurants = get_restaurant_suggestions(latitude, longitude, range=3)
    if restaurants:
        print("提案されたお店:")
        for idx, restaurant in enumerate(restaurants, 1):
            print(f"{idx}. {restaurant['name']} ({restaurant['genre']}) - {restaurant['address']}")
            print(f"   URL: {restaurant['url']}")
    else:
        print("お店情報の取得に失敗しました。")