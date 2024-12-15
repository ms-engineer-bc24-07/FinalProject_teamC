# api/serializers/user_profile_serializer.py
from rest_framework import serializers
from api.models import UserProfile  # 変更後のインポート方法

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
