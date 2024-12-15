# api/serializers/participation_serializer.py

from api.models.participation_model import Participation
from api.serializers.user_profile_serializer import UserProfileSerializer
from rest_framework import serializers


class ParticipationSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer()  # UserProfileSerializerをネスト

    class Meta:
        model = Participation
        fields = "__all__"  # 全フィールドをシリアライズ
