import os
import openai
import requests
from dotenv import load_dotenv
import logging

# ロギングの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
                    "address": f"{station}駅",  # 駅名を検索
                    "key": VenueService.GOOGLE_MAPS_API_KEY,  # APIキー
                },
            )
            response.raise_for_status()
            data = response.json()

            # レスポンスの構造をデバッグ
            logger.info(f"Google Maps API response: {data}")

            if not data.get("results"):
                raise ValueError(f"座標が見つかりませんでした: {station}駅")

            location = data["results"][0]["geometry"]["location"]
            return location
        except Exception as e:
            logger.error(f"座標取得中にエラーが発生しました: {e}")
            raise ValueError(f"座標取得中にエラーが発生しました: {e}")

    @staticmethod
    def get_midpoint_for_group(group_stations):
        """グループの最寄駅情報を元に座標を取得し、中間地点を計算"""
        coordinates = []

        # 各最寄駅の座標を取得
        for station in group_stations:
            coordinates.append(VenueService.get_coordinates(station))

        # 中間地点を計算
        lat = sum(coord["lat"] for coord in coordinates) / len(coordinates)
        lng = sum(coord["lng"] for coord in coordinates) / len(coordinates)

        return lat, lng

    @staticmethod
    def search_restaurants(midpoint, venue_preference):
        """中間地点付近のお店をホットペッパーAPIで検索"""
        if not midpoint or len(midpoint) != 2:
            raise ValueError("中間地点(midpoint)は (lat, lng) の形式で指定してください。")

        if not venue_preference or not isinstance(venue_preference, str):
            raise ValueError("venue_preference は有効なキーワード文字列で指定してください。")

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

            # レスポンスデータの確認
            logger.info(f"HotPepper API response: {data}")

            # APIレスポンスの検証
            if not data.get("results"):
                raise ValueError("店舗情報が見つかりませんでした。")

            return data["results"]  # ここはリストのままでOK
        except requests.exceptions.Timeout:
            logger.error("HotPepper API リクエストがタイムアウトしました。")
            raise RuntimeError("HotPepper API リクエストがタイムアウトしました。")
        except requests.exceptions.RequestException as e:
            logger.error(f"HotPepper API リクエストエラー: {e}")
            raise RuntimeError(f"HotPepper API リクエストエラー: {e}")
        except ValueError as e:
            logger.error(f"HotPepper API レスポンスエラー: {e}")
            raise RuntimeError(f"HotPepper API レスポンスエラー: {e}")

    @staticmethod
    def recommend_top_venues(shops):
        """OpenAI APIでお店リストから3つのおすすめを生成"""
        try:
            # 店舗情報を確認
            if not shops or not isinstance(shops, list):
                raise ValueError("店舗情報が正しく提供されていません。")

            # 店舗情報をまとめる
            shop_descriptions = []
            for shop in shops:
                try:
                    name = shop.get('name')
                    genre = shop.get('genre', {}).get('name')
                    address = shop.get('address')

                    # 必要な情報が欠けている場合、エラーメッセージを表示してスキップ
                    if not name or not genre or not address:
                        logger.warning(f"警告: 必要な情報が欠けています: {shop}")
                        continue  # 情報が欠けている店舗はスキップ

                    shop_descriptions.append(f"店名: {name}, ジャンル: {genre}, 住所: {address}")
                except Exception as e:
                    logger.error(f"店舗情報の処理中にエラーが発生しました: {e}")
                    continue  # エラーが発生した場合はスキップ

            if not shop_descriptions:
                raise ValueError("有効な店舗情報がありません。")

            # OpenAI APIへのプロンプト
            prompt = (
                "以下のお店の中から、最もおすすめの3つを提案してください。\n\n"
                + "\n".join(
                    f"{i + 1}. {desc}" for i, desc in enumerate(shop_descriptions)
                )
                + "\n\n提案結果:"
            )

            # OpenAI API呼び出し
            response = openai.ChatCompletion.create(
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

            # レスポンスを表示（デバッグ用）
            logger.info(f"OpenAI API Response: {response}")

            # レスポンスの構造が予想通りでない場合に備えて修正
            choices_content = response['choices'][0]['message']['content'] if 'choices' in response else None

            if not choices_content:
                raise ValueError("OpenAI APIのレスポンスに推奨店舗が含まれていません。")

            return choices_content
        except Exception as e:
            logger.error(f"OpenAI APIエラーの詳細: {str(e)}")
            raise RuntimeError(f"OpenAI APIエラー: {e}")


    @staticmethod
    def get_venue_suggestions_for_group(group, shop_atmosphere_preference):
        """グループの最寄り駅を元に中間地点を計算し、店舗を提案する"""
        try:
            # グループの最寄り駅情報を取得
            if not group or not isinstance(group, list):
                raise ValueError("グループ情報が正しく提供されていません。")

            stations = [user.station for user in group if hasattr(user, 'station')]  # 各ユーザーの最寄り駅をリストに

            if not stations:
                raise ValueError("グループの最寄り駅情報が正しく提供されていません。")

            # 各駅の座標を取得
            coordinates = [VenueService.get_coordinates(station) for station in stations]

            # 中間地点を算出
            midpoint = VenueService.get_midpoint_for_group(stations)

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
        except Exception as e:
            logger.error(f"店舗提案中にエラーが発生しました: {e}")
            raise RuntimeError(f"店舗提案中にエラーが発生しました: {e}")
