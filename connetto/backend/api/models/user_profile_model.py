# api/models/user_profile_model.py
# ユーザー情報モデル
from django.db import models

GENDER_CHOICES = [
    ("male", "男性"),
    ("female", "女性"),
]


class UserProfile(models.Model):
    username = models.CharField(max_length=50)
    full_name = models.CharField(max_length=100)
    furigana = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    birth_year = models.IntegerField()  # 生まれ年（西暦）
    join_year = models.IntegerField()  # 入社年（西暦）
    department = models.CharField(max_length=50)  # 部署
    station = models.CharField(max_length=50)
    # email = models.EmailField(unique=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
