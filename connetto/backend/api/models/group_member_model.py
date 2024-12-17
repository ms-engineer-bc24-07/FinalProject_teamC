# グループメンバー情報モデル
# api/models/group_member_model.py

from django.contrib.auth.models import User  # Djangoのデフォルトユーザーモデルを使用
from django.db import models

from .group_model import Group


class GroupMember(models.Model):
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="members"
    )  # グループID（リレーション）
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="group_memberships"
    )  # ユーザーID（リレーション）
    joined_at = models.DateTimeField(
        auto_now_add=True
    )  # メンバーがグループに追加された日時

    def __str__(self):
        return f"{self.user.username} in {self.group.name}"
