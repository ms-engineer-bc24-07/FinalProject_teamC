# 店候補情報サービス
# backend/api/services/venue_service.py

import os

import requests
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()


class VenueService:
    GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
    HOTPEPPER_API_KEY = os.getenv("HOTPEPPER_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    @staticmethod
    def get_coordinates(station):
        """最寄り駅から座標を取得"""
        try:
            response = requests.get(
                "https://maps.googleapis.com/maps/api/geocode/json",
                params={
                    "address": f"{station}駅",
                    "key": VenueService.GOOGLE_MAPS_API_KEY,
                },
            )
            response.raise_for_status()
            data = response.json()

            if not data["results"]:
                raise ValueError("座標が見つかりませんでした。")

            location = data()["results"][0]["geometry"]["location"]
            return location["lat"], location["lng"]
        except (requests.RequestException, ValueError) as e:
            raise RuntimeError(f"Google Maps APIエラー: {e}")

    @staticmethod
    def calculate_midpoint(coordinates):
        """複数の座標から中間地点を算出"""
        if not coordinates:
            raise ValueError("座標リストが空です。")

        lat = sum(coord["lat"] for coord in coordinates) / len(coordinates)
        lng = sum(coord["lng"] for coord in coordinates)
        return lat, lng

    @staticmethod
    def search_restaurants(midpoint, venue_preference):
        """中間地点付近のお店をホットペッパーAPIで検索"""
        if not midpoint or len(midpoint) != 2:
            raise ValueError(
                "中間地点(midpoint)は (lat, lng) の形式で指定してください。"
            )

        if not venue_preference or not isinstance(venue_preference, str):
            raise ValueError(
                "venue_preference は有効なキーワード文字列で指定してください。"
            )

        api_url = ("https://webservice.recruit.co.jp/hotpepper/gourmet/v1/",)
        params = (
            {
                "key": VenueService.HOTPEPPER_API_KEY,
                "lat": midpoint[0],  # 緯度
                "lng": midpoint[1],  # 経度
                "range": 3,  # 検索範囲（3km）
                "keyword": venue_preference,  # 検索キーワード
                "format": "json",  # レスポンス形式
            },
        )
        try:
            response = requests.get(api_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            # APIレスポンスの検証
            if "results" not in data or "shop" not in data["results"]:
                raise ValueError("店舗情報が見つかりませんでした。")

            return data["results"]["shop"]

        except requests.exceptions.Timeout:
            raise RuntimeError("HotPepper API リクエストがタイムアウトしました。")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"HotPepper API リクエストエラー: {e}")
        except ValueError as e:
            raise RuntimeError(f"HotPepper API レスポンスエラー: {e}")
