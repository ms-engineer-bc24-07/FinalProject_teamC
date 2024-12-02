# api/models/user_model.py
# ユーザー情報モデル
from django.db import models


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=255)
    birth_year = models.IntegerField()  # 生まれ年（西暦）
    gender = models.CharField(
        max_length=10, choices=[("male", "男性"), ("female", "女性")]
    )  # 性別
    department = models.CharField(
        max_length=50,
        choices=[
            ("sales", "営業部"),
            ("planning", "企画部"),
            ("general_affairs", "総務部"),
            ("hr", "人事部"),
            ("manufacturing", "製造部"),
            ("development", "開発部"),
        ],
    )  # 部署
    joining_year = models.IntegerField()  # 入社年（西暦）

    def __str__(self):
        return self.name
