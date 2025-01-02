from rest_framework import serializers
from api.models.group_member_model import GroupMember

class GroupMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMember
        fields = '__all__'