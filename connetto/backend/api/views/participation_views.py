from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from api.models.participation_model import Participation
from api.serializers.participation_serializer import ParticipationSerializer
from api.models.notification_model import Notification, NotificationType
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from connetto_backend.firebase import verify_firebase_token  # Firebaseトークン検証関数をインポート
from django.utils import timezone
from django.db.models import Q

class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        authorization_header = request.headers.get("Authorization")
        if not authorization_header or not authorization_header.startswith("Bearer "):
            return None

        token = authorization_header.split("Bearer ")[1]
        try:
            decoded_token = verify_firebase_token(token)
            uid = decoded_token["uid"]

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


class ParticipationView(APIView):
    authentication_classes = [FirebaseAuthentication] 
    permission_classes = [IsAuthenticated]  

    def post(self, request):
        print("受信データ:", request.data)

        user = request.user
        print("認証されたユーザー:", user.username)
        
        data = request.data.copy()
        data["user"] = user.id 

        serializer = ParticipationSerializer(data=data)
        if serializer.is_valid():
            participation = serializer.save()
            print("バリデーション成功:", serializer.validated_data)

            Notification.objects.create(
                user=user,
                title="【登録完了】",
                body="行きたい登録が完了しました！ありがとうございます。内容の変更や削除は申込内容確認画面から行うことができます。",
                notification_type=NotificationType.REGISTER,
                data={"participation_id": participation.id},
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print("バリデーションエラー:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        try:
            print("GETリクエストを受信しました")
            print("認証済みユーザー:", request.user.username)

            pk = kwargs.get('pk')
            print("取得するPK:", pk)

            if pk:
                participation = Participation.objects.get(id=pk, user=request.user)
                print("参加情報を取得しました:", participation)
                serializer = ParticipationSerializer(participation)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            participations = Participation.objects.filter(user=request.user).order_by('-created_at')
            print("フィルタリング後の参加情報:", participations)

            serializer = ParticipationSerializer(participations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Participation.DoesNotExist:
            return Response({"detail": "指定されたデータが存在しません。"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print("サーバーエラー:", e)
            return Response({"detail": "サーバーエラーが発生しました。"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def put(self, request, pk):
        try:
            participation = Participation.objects.get(pk=pk, user=request.user)
        except Participation.DoesNotExist:
            return Response({"detail": "該当する登録内容が見つかりません。"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ParticipationSerializer(participation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            Notification.objects.create(
                user=request.user,
                title="【変更完了】",
                body="登録内容が変更されました。内容をご確認ください。",
                notification_type=NotificationType.UPDATE,
                data={"participation_id": participation.id},
            )
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            participation = Participation.objects.get(pk=pk, user=request.user)
        except Participation.DoesNotExist:
            return Response({"detail": "該当する登録内容が見つかりません。"}, status=status.HTTP_404_NOT_FOUND)

        participation.delete()
        Notification.objects.create(
            user=request.user,
            title="【削除完了】",
            body="登録内容が削除されました。",
            notification_type=NotificationType.DELETE,
                data={"participation_id": participation.id},
        )
        return Response({"detail": "登録内容が削除されました。"}, status=status.HTTP_204_NO_CONTENT)