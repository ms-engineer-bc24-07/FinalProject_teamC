# backend/api/views/venue_views.py

from api.services.venue_service import VenueService
from connetto_backend.firebase import verify_firebase_token
from rest_framework import status
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


# Firebase認証クラスの再利用
class FirebaseUser:
    def __init__(self, decoded_token):
        self.uid = decoded_token["uid"]
        self.email = decoded_token.get("email", "")
        self.decoded_token = decoded_token
        self.is_authenticated = True


class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        authorization_header = request.headers.get("Authorization")
        if not authorization_header or not authorization_header.startswith("Bearer "):
            raise AuthenticationFailed("Authorization header missing or invalid")

        token = authorization_header.split("Bearer ")[1]
        try:
            decoded_token = verify_firebase_token(token)  # トークン検証
            user = FirebaseUser(decoded_token)
            return (user, None)
        except ValueError as e:
            # エラーの詳細を含めて AuthenticationFailed を発生
            raise AuthenticationFailed(f"Token verification failed: {str(e)}")
        except Exception as e:
            # ログに記録して一般的なエラーメッセージを返す
            import logging

            logger = logging.getLogger(__name__)
            logger.error(f"Unexpected error during token verification: {e}")

            raise AuthenticationFailed(
                "An unexpected error occurred during token verification"
            )


class VenueView(APIView):
    authentication_classes = [FirebaseAuthentication]  # Firebase認証を使用
    permission_classes = [IsAuthenticated]  # 認証されたユーザーのみアクセス可能

    def post(self, request):
        """複数の駅を基に中間地点と周辺のおすすめ店舗を提案する"""
        try:
            # リクエストユーザー情報（必要であれば使用）
            user_data = request.user  # FirebaseUserオブジェクト
            uid = user_data.uid  # UIDを取得
            print("UID:", uid)

            # リクエストデータを取得
            body = request.data
            stations = body.get("stations", [])
            venue_preference = body.get("venue_preference", "")

            if not stations or not venue_preference:
                return Response(
                    {"error": "stations と venue_preference を指定してください。"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # 1. 各駅の座標を取得
            coordinates = [
                VenueService.get_coordinates(station) for station in stations
            ]

            # 2. 中間地点の計算
            midpoint = VenueService.calculate_midpoint(coordinates)

            # 3. ホットペッパーでお店検索
            shops = VenueService.search_restaurants(midpoint, venue_preference)

            if not shops:
                return Response(
                    {"error": "近くにお店が見つかりませんでした。"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # 4. OpenAIでおすすめの店舗を提案
            recommendations = VenueService.recommend_top_venues(shops)

            return Response(
                {"recommendations": recommendations}, status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": f"サーバーエラー: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
