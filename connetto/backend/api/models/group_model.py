# グループ情報モデル
# api/models/group_model.py

from django.contrib.auth.models import User  # Djangoのデフォルトユーザーモデルを使用
from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)  # グループ名（ユニーク）
    meeting_date = models.DateField()  # 飲み会の日付
    leader = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="led_groups"
    )  # グループのリーダー（幹事）
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時
    updated_at = models.DateTimeField(auto_now=True)  # 更新日時

    def __str__(self):
        return f"Group {self.name} on {self.meeting_date}"
