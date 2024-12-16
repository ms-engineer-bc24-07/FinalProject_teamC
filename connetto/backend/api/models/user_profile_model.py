# api/models/user_profile_model.py
# ユーザー情報モデル
from django.contrib.auth.models import User  # Djangoのデフォルトユーザーモデルを使用
from django.db import models

GENDER_CHOICES = [
    ("male", "男性"),
    ("female", "女性"),
]

class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
    username = models.CharField(max_length=50)
    full_name = models.CharField(max_length=100)
    furigana = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    birth_year = models.IntegerField()  # 生まれ年（西暦）
    company = models.CharField(max_length=100)  # 企業情報を保持
    join_year = models.IntegerField()  # 入社年（西暦）
    department = models.CharField(max_length=50)  # 部署
    station = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
