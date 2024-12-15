from django.db import models
from django.core.validators import MinValueValidator
from datetime import datetime

class User(models.Model):
    name = models.CharField(max_length=255)
    company = models.CharField(max_length=100)  # 企業情報を保持
    birth_year = models.IntegerField(
        validators=[MinValueValidator(1900)]  # 1900年以降の年に制限
    )  # 生まれ年（西暦）
    gender = models.CharField(
        max_length=10, 
        choices=[
            ("male", "男性"),
            ("female", "女性"),
            ("other", "その他"),  # 選択肢を増加
        ]
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
    joining_year = models.IntegerField(
        validators=[MinValueValidator(1900)]  # 1900年以降の年に制限
    )  # 入社年（西暦）

    def __str__(self):
        return f"{self.name} ({self.department}, {self.company})"
