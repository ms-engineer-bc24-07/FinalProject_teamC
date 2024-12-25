# backend/api/views/participation_views.py

from api.models.notification_model import Notification
from api.models.participation_model import Participation
from api.serializers.participation_serializer import ParticipationSerializer
from connetto_backend.firebase import verify_firebase_token  # Firebaseトークン検証関数をインポート
from django.contrib.auth.models import User
from django.utils import timezone
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
            participation = serializer.save()
            print("バリデーション成功:", serializer.validated_data)

            # 通知を作成
            Notification.objects.create(
                user=user,
                title="【登録完了】",
                body="行きたい登録が完了しました！ありがとうございます。内容の変更や削除は申込内容確認画面から行うことができます。",
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print("バリデーションエラー:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        try:
            pk = kwargs.get("pk")

            if pk:
                participation = Participation.objects.get(id=pk, user=request.user)
                serializer = ParticipationSerializer(participation)
                return Response(serializer.data, status=status.HTTP_200_OK)

            today = timezone.now().date()
            participations = Participation.objects.filter(
                desired_dates__gte=today, user=request.user
            ).order_by("-created_at")
            serializer = ParticipationSerializer(participations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Participation.DoesNotExist:
            return Response(
                {"detail": "指定されたデータが存在しません。"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            print("サーバーエラー:", e)
            return Response(
                {"detail": "サーバーエラーが発生しました。"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request, pk):
        try:
            participation = Participation.objects.get(pk=pk, user=request.user)
        except Participation.DoesNotExist:
            return Response(
                {"detail": "該当する登録内容が見つかりません。"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ParticipationSerializer(
            participation, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            Notification.objects.create(
                user=request.user,
                title="【変更完了】",
                body="登録内容が変更されました。内容をご確認ください。",
            )
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            participation = Participation.objects.get(pk=pk, user=request.user)
        except Participation.DoesNotExist:
            return Response(
                {"detail": "該当する登録内容が見つかりません。"},
                status=status.HTTP_404_NOT_FOUND,
            )

        participation.delete()
        Notification.objects.create(
            user=request.user,
            title="【削除完了】",
            body="登録内容が削除されました。",
        )
        return Response(
            {"detail": "登録内容が削除されました。"}, status=status.HTTP_204_NO_CONTENT
        )
