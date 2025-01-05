from rest_framework import serializers
from api.models.group_model import Group
from api.models.group_member_model import GroupMember
from api.serializers.group_member_serializer import GroupMemberSerializer

class GroupSerializer(serializers.ModelSerializer):
    number_of_members = serializers.SerializerMethodField()
    members = GroupMemberSerializer(many=True, read_only=True) 

    class Meta:
        model = Group
        fields = ['identifier', 'meeting_date', 'meeting_location', 'number_of_members','members']  # 必要なフィールドを指定

    def get_number_of_members(self, obj):
        return GroupMember.objects.filter(group=obj).count() 