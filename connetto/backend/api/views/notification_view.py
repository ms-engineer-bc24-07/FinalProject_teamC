from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from api.models.notification_model import Notification
from api.serializers.notification_serializer import NotificationSerializer
from connetto_backend.firebase import verify_firebase_token
from django.contrib.auth.models import User


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
                username=uid,
                defaults={"email": decoded_token.get("email", "")}
            )
            if created:
                print(f"新しいユーザーを作成しました: {user.username}")
            return (user, None)
        except ValueError:
            raise AuthenticationFailed("Invalid Firebase token.")
        except Exception:
            raise AuthenticationFailed("Authentication failed.")


class NotificationView(APIView):
    authentication_classes = [FirebaseAuthentication]  # Firebase認証
    permission_classes = [IsAuthenticated]  # 認証必須

    def get(self, request):
        user = request.user  # 認証されたユーザーを取得
        notifications = Notification.objects.filter(user=user).order_by('-created_at')  # ユーザーの通知を取得
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class NotificationDetailView(APIView):
    authentication_classes = [FirebaseAuthentication]  
    permission_classes = [IsAuthenticated]  

    def get(self, request, notification_id):
        notification = Notification.objects.filter(user=request.user, id=notification_id).first()
        if not notification:
            return Response({"detail": "通知が見つかりませんでした。"}, status=status.HTTP_404_NOT_FOUND)
        serializer = NotificationSerializer(notification)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, notification_id):
        notification = Notification.objects.filter(user=request.user, id=notification_id).first()
        if not notification:
            return Response({"detail": "通知が見つかりませんでした。"}, status=status.HTTP_404_NOT_FOUND)
        notification.is_read = True
        notification.save()
        return Response({"message": "通知を既読にしました。"}, status=status.HTTP_200_OK)
