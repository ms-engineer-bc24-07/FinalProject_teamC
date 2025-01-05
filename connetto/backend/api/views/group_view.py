from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.models.group_model import Group
from api.models.group_member_model import GroupMember
from api.serializers.group_serializer import GroupSerializer
from connetto_backend.firebase import verify_firebase_token
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User

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

class GroupListView(APIView):
    authentication_classes = [FirebaseAuthentication]  # Firebase認証を適用
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        groups = Group.objects.filter(members__user=user).distinct().order_by('meeting_date') 

        # デバッグコードを追加
        for group in groups:
            print(f"Group: {group.identifier}, Members: {group.members.all()}")

        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)


