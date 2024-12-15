# backend/api/views/user_profile_views.py
from api.models.user_profile_model import UserProfile
from api.serializers.user_profile_serializer import UserProfileSerializer
from connetto_backend.firebase import verify_firebase_token
from rest_framework import status
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


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
            raise AuthenticationFailed(str(e))
        except Exception:
            raise AuthenticationFailed(
                "An unexpected error occurred during token verification"
            )


class UserProfileView(APIView):
    authentication_classes = [FirebaseAuthentication]  # Firebase認証を有効にする
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("リクエストヘッダー:", request.headers)

        user_data = request.user  # FirebaseUserオブジェクト
        print("認証されたユーザー情報:", user_data.decoded_token)

        uid = user_data.uid
        print("UID:", uid)

        data = request.data.copy()
        data["username"] = uid

        serializer = UserProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        uid = request.user.uid  # FirebaseUserクラスを使用してUIDを取得
        try:
            profile = UserProfile.objects.get(username=uid)
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response(
                {"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND
            )
