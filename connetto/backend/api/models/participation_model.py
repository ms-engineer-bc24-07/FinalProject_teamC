# api/models/participation_model.py

from datetime import datetime

# from django.contrib.auth.models import User  # Djangoのデフォルトユーザーモデルを使用
from api.models.user_profile_model import UserProfile
from django.core.validators import MinValueValidator  # これを追加
from django.db import models


class Participation(models.Model):
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="participations"
    )
    # date = models.DateField()  # 希望日
    # time = models.TimeField()  # 希望時間
    gender_restriction = models.CharField(
        max_length=50,
        choices=[("same_gender", "同性"), ("no_restriction", "希望なし")],
        default="no_restriction",
    )
    age_restriction = models.CharField(
        max_length=50,
        choices=[
            ("same_age", "同年代"),
            ("broad_age", "幅広い年代"),
            ("no_restriction", "希望なし"),
        ],
        default="no_restriction",
    )
    joining_year_restriction = models.CharField(
        max_length=50,
        choices=[("exact_match", "同期のみ"), ("no_restriction", "希望なし")],
        default="no_restriction",
    )
    department_restriction = models.CharField(
        max_length=50,
        choices=[
            ("same_department", "所属部署内希望"),
            ("mixed_departments", "他部署混在"),
            ("no_restriction", "希望なし"),
        ],
        default="no_restriction",
    )
    atmosphere_preference = models.CharField(
        max_length=50,
        choices=[
            ("quiet", "落ち着いたお店"),
            ("lively", "わいわいできるお店"),
            ("no_restriction", "希望なし"),
        ],
        default="no_restriction",
    )
    desired_dates = models.JSONField(
        validators=[
            MinValueValidator(datetime.today().date())
        ]  # これでエラーが解消されるはず
    )  # 希望日時をリスト形式で保存可能

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # desired_dates の最初の値を date と time に同期
        # if self.desired_dates and isinstance(self.desired_dates[0], dict):
        #     first_entry = self.desired_dates[0]
        #     self.date = first_entry.get("date", self.date)
        #     self.time = first_entry.get("time", self.time)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Participation by {self.user.username} on {self.created_at}"
