import requests
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

load_dotenv()

def test_google_maps_api():
    """
    Google Maps APIを使用して、地名の緯度・経度を取得するテスト関数。
    """
    try:
        google_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        if not google_api_key:
            logging.error("Google APIキーが見つかりません。.envファイルにGOOGLE_API_KEYを設定してください。")
            return

        location_name = "川崎駅"

        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "address": location_name,
            "key": google_api_key,
        }

        logging.info(f"{location_name}の緯度・経度を取得中...")
        response = requests.get(url, params=params)

        if response.status_code == 200:
            results = response.json().get("results", [])
            if results:
                location = results[0]["geometry"]["location"]
                latitude, longitude = location["lat"], location["lng"]
                logging.info(f"{location_name}の緯度: {latitude}, 経度: {longitude}")
            else:
                logging.error(f"{location_name}に該当する結果が見つかりません。")
        else:
            logging.error(f"Google Maps APIリクエストエラー: {response.status_code}")

    except Exception as e:
        logging.error(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    test_google_maps_api()