# backend/models/group_model.py
# Group情報を管理、GroupMemberでグループとそのメンバーを関連付ける

from django.db import models
from django.contrib.auth.models import User  # Userモデルをインポート

class Group(models.Model):
    name = models.CharField(max_length=100)  # グループ名（任意）
    group_date = models.DateTimeField()  # グループ作成日時
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時

    def __str__(self):
        return self.name


class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_members')
    role = models.CharField(max_length=50, default="member")  # メンバーの役割（任意）

    def __str__(self):
        return f"{self.user.username} in {self.group.name}"
