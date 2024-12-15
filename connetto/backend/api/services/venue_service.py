# 店候補情報サービス
# backend/api/services/venue_service.py

import os

import openai
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
                raise ValueError("座標が見つかりませんでした。:{station}駅")

            location = data["results"][0]["geometry"]["location"]
            return location["lat"], location["lng"]
        except (requests.RequestException, ValueError) as e:
            raise RuntimeError(f"Google Maps APIエラー: {e}")

    @staticmethod
    def calculate_midpoint(coordinates):
        """複数の座標から中間地点を算出"""
        if not coordinates:
            raise ValueError("座標リストが空です。")

        lat = sum(coord["lat"] for coord in coordinates) / len(coordinates)
        lng = sum(coord["lng"] for coord in coordinates) / len(coordinates)
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

        api_url = "https://webservice.recruit.co.jp/hotpepper/gourmet/v1/"
        params = {
            "key": VenueService.HOTPEPPER_API_KEY,
            "lat": midpoint[0],  # 緯度
            "lng": midpoint[1],  # 経度
            "range": 3,  # 検索範囲（3km）
            "keyword": venue_preference,  # 検索キーワード
            "format": "json",  # レスポンス形式
        }

        try:
            response = requests.get(api_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            # APIレスポンスの検証
            if not data.get("results") or not data["results"].get("shop"):
                raise ValueError("店舗情報が見つかりませんでした。")

            return data["results"]["shop"]
        except requests.exceptions.Timeout:
            raise RuntimeError("HotPepper API リクエストがタイムアウトしました。")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"HotPepper API リクエストエラー: {e}")
        except ValueError as e:
            raise RuntimeError(f"HotPepper API レスポンスエラー: {e}")

    @staticmethod
    def recommend_top_venues(shops):
        """OpenAI APIでお店リストから3つのおすすめを生成"""
        try:
            # 店舗情報をまとめる
            shop_descriptions = [
                f"店名: {shop['name']}, ジャンル: {shop['genre']['name']}, 住所: {shop['address']}"
                for shop in shops
            ]

            # OpenAI APIへのプロンプト
            prompt = (
                "以下のお店の中から、最もおすすめの3つを提案してください。\n\n"
                + "\n".join(
                    f"{i + 1}. {desc}" for i, desc in enumerate(shop_descriptions)
                )
                + "\n\n提案結果:"
            )

            # OpenAI API呼び出し
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

            if not response.choices or not response.choices[0].message.content.strip():
                raise ValueError("OpenAI APIのレスポンスが不正です。")

            # 結果を取得
            recommendations = response.choices[0].message.content.strip()
            return recommendations
        except Exception as e:
            raise RuntimeError(f"OpenAI APIエラー: {e}")

    @staticmethod
    def get_venue_suggestions_for_group(group, shop_atmosphere_preference):
        """グループの最寄り駅を元に中間地点を計算し、店舗を提案する"""
        # グループの最寄り駅情報を取得
        stations = [user.station for user in group]  # 各ユーザーの最寄り駅をリストに

        # 各駅の座標を取得
        coordinates = [VenueService.get_coordinates(station) for station in stations]

        # 中間地点を算出
        midpoint = VenueService.calculate_midpoint(coordinates)

        # お店の雰囲気の条件に基づいて検索キーワードを設定
        if shop_atmosphere_preference == "calm":
            venue_preference = "落ち着いたお店"
        elif shop_atmosphere_preference == "lively":
            venue_preference = "わいわいできるお店"
        else:
            venue_preference = "希望なし"  # もし指定がない場合

        # お店を検索
        shops = VenueService.search_restaurants(midpoint, venue_preference)

        # おすすめのお店をOpenAIで取得
        top_venues = VenueService.recommend_top_venues(shops)

        return top_venues
