# api/serializers/user_profile_serializer.py

from api.models.user_profile_model import UserProfile
from rest_framework import serializers


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"
