# 店候補情報サービス
# backend/api/services/venue_service.py

import requests


class VenueService:
    GOOGLE_MAPS_API_KEY = "YOUR_GOOGLE_MAPS_API_KEY"
    HOTPEPPER_API_KEY = "YOUR_HOTPEPPER_API_KEY"

    @staticmethod
    def get_coordinates(station):
        """最寄り駅から座標を取得"""
        response = requests.get(
            "https://maps.googleapis.com/maps/api/geocode/json",
            params={"address": f"{station}駅", "key": VenueService.GOOGLE_MAPS_API_KEY},
        )
        location = response.json()["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]

    @staticmethod
    def calculate_midpoint(coordinates):
        """複数の座標から中間地点を算出"""
        lat = sum(coord["lat"] for coord in coordinates) / len(coordinates)
        lng = sum(coord["lng"] for coord in coordinates) / len(coordinates)
        return lat, lng

    @staticmethod
    def search_restaurants(midpoint, venue_preference):
        """中間地点付近のお店をホットペッパーAPIで検索"""
        response = requests.get(
            "https://webservice.recruit.co.jp/hotpepper/gourmet/v1/",
            params={
                "key": VenueService.HOTPEPPER_API_KEY,
                "lat": midpoint[0],
                "lng": midpoint[1],
                "range": 3,
                "keyword": venue_preference,
                "format": "json",
            },
        )
        return response.json()["results"]["shop"]
