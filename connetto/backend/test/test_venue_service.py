from unittest.mock import patch, MagicMock
import pytest
from api.services.venue_service import VenueService

@pytest.mark.django_db
@patch("api.services.venue_service.openai.ChatCompletion.create")
@patch("api.services.venue_service.requests.get")
def test_venue_service(mock_requests_get, mock_openai_create):
    try:
        # モックされたAPIレスポンスの設定
        # 各最寄駅に対する座標をモック
        mock_requests_get.return_value.json.return_value = {
            "results": [
                {"geometry": {"location": {"lat": 35.6844, "lng": 139.7034}}},  # 新宿御苑前駅の座標
                {"geometry": {"location": {"lat": 35.7028, "lng": 139.6608}}},  # 中野駅の座標
                {"geometry": {"location": {"lat": 35.0332, "lng": 139.6585}}},  # 三軒茶屋駅の座標
                {"geometry": {"location": {"lat": 35.7328, "lng": 139.7117}}},  # 池袋駅の座標
            ]
        }

        # OpenAI APIレスポンスのモック
        mock_openai_create.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "1. レストランA (和食): 東京都渋谷区\n2. レストランB (イタリアン): 東京都新宿区\n3. レストランC (カフェ): 東京都池袋区"
                    }
                }
            ]
        }

        # モックユーザーオブジェクトの作成（4人分）
        user1 = MagicMock()
        user1.station = "新宿御苑前駅"

        user2 = MagicMock()
        user2.station = "中野駅"

        user3 = MagicMock()
        user3.station = "三軒茶屋駅"

        user4 = MagicMock()
        user4.station = "池袋駅"

        group = [user1, user2, user3, user4]  # 4人のユーザーオブジェクトのリスト

        shop_atmosphere_preference = "cozy"

        # サービスを使用して店舗の提案を取得
        suggestions = VenueService.get_venue_suggestions_for_group(group, shop_atmosphere_preference)

        # 提案された店舗情報のテスト
        assert len(suggestions) > 0, "提案された店舗がありません"
        assert isinstance(suggestions, str), "提案は文字列として返されるべきです"
        assert suggestions.strip(), "提案された店舗情報が空です"

    except Exception as e:
        pytest.fail(f"エラーが発生しました: {e}")
