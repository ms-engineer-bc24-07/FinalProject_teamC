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
    def get_venue_suggestions_for_group(group, shop_atmosphere_preference):
        """グループの最寄り駅を元に中間地点を計算し、店舗を提案する"""
        try:
            # グループの最寄り駅情報を取得
            if not group or not isinstance(group, list):
                raise ValueError("グループ情報が正しく提供されていません。")

            stations = [user.station for user in group if hasattr(user, 'station')]  # 各ユーザーの最寄り駅をリストに

            if not stations:
                raise ValueError("グループの最寄り駅情報が正しく提供されていません。")

            # 東京駅の座標を手動で指定
            midpoint = [35.681236, 139.767125]  # 東京駅の座標

            # お店の雰囲気の条件に基づいて検索キーワードを設定
            if shop_atmosphere_preference == "calm":
                venue_preference = "居酒屋"  # ここを「居酒屋」に変更
            elif shop_atmosphere_preference == "lively":
                venue_preference = "居酒屋"  # こちらも「居酒屋」
            else:
                venue_preference = "居酒屋"  # 何も指定されていない場合も居酒屋

            # お店を検索
            shops = VenueService.search_restaurants(midpoint, venue_preference)

            # 検索結果を表示
            return shops
        except Exception as e:
            logger.error(f"店舗提案中にエラーが発生しました: {e}")
            raise RuntimeError(f"店舗提案中にエラーが発生しました: {e}")


# 実行コード部分
if __name__ == "__main__":
    group = [
        type("User", (), {"station": "東京"}),  # 仮のグループ情報
    ]
    shop_atmosphere_preference = "居酒屋"  # 居酒屋を探す

    try:
        top_venues = VenueService.get_venue_suggestions_for_group(group, shop_atmosphere_preference)
        print("おすすめのお店:", top_venues)
    except Exception as e:
        print(f"エラーが発生しました: {e}")
