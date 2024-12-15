# backend/api/views/participation_views.py
from api.models.participation_model import Participation
from api.serializers.participation_serializer import ParticipationSerializer
from connetto_backend.firebase import verify_firebase_token  # Firebaseトークン検証関数をインポート
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Authorizationヘッダーからトークンを取得
        authorization_header = request.headers.get("Authorization")
        if not authorization_header or not authorization_header.startswith("Bearer "):
            return None

        token = authorization_header.split("Bearer ")[1]
        try:
            # Firebaseトークンを検証してUIDを取得
            decoded_token = verify_firebase_token(token)
            uid = decoded_token["uid"]

            # UIDに対応するDjangoユーザーを取得または作成
            user, created = User.objects.get_or_create(
                username=uid, defaults={"email": decoded_token.get("email", "")}
            )
            if created:
                print(f"新しいユーザーを作成しました: {user.username}")
            return (user, None)
        except ValueError:
            raise AuthenticationFailed("Invalid Firebase token.")
        except Exception:
            raise AuthenticationFailed("Authentication failed.")


class ParticipationView(APIView):
    authentication_classes = [FirebaseAuthentication]  # Firebase認証を利用
    permission_classes = [IsAuthenticated]  # 認証必須

    def post(self, request):
        print("受信データ:", request.data)

        # 認証されたユーザー情報を利用
        user = request.user
        print("認証されたユーザー:", user.username)

        # リクエストデータをコピーして、ユーザー情報を追加
        data = request.data.copy()
        data["user"] = user.id  # 認証されたユーザーのIDを設定

        serializer = ParticipationSerializer(data=data)
        if serializer.is_valid():
            print("バリデーション成功:", serializer.validated_data)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print("バリデーションエラー:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        # 認証されたユーザーに関連するデータのみを返す
        participations = Participation.objects.filter(user=request.user)
        serializer = ParticipationSerializer(participations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
