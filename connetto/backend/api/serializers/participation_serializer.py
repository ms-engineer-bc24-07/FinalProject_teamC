# api/serializers/participation_serializer.py

from rest_framework import serializers
from api.models.participation_model import Participation
from datetime import datetime
from pytz import UTC

class ParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participation
        fields = '__all__'

    def validate_desired_dates(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("希望日はリスト形式で指定してください。")

        for date_str in value:
            try:
                date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                if date <= datetime.now(UTC):
                    raise serializers.ValidationError(f"希望日は未来の日付である必要があります: {date_str}")
            except ValueError:
                raise serializers.ValidationError(f"日付の形式が正しくありません: {date_str}")

        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if "desired_dates" in representation:
            representation["desired_dates"] = [
                datetime.fromisoformat(date.replace('Z', '+00:00')).astimezone().isoformat()
                for date in representation["desired_dates"]
            ]
        return representation
