# api/serializers/participation_serializer.py

from api.models.participation_model import Participation
from rest_framework import serializers


class ParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participation
        fields = "__all__"  # 全フィールドをシリアライズ
