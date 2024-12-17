# api/models/participation_model.py

from datetime import datetime  # これも追加

from django.contrib.auth.models import User  # Djangoのデフォルトユーザーモデルを使用
from django.core.validators import MinValueValidator  # これを追加
from django.db import models
from django.utils import timezone  # 仮


class Participation(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="participations"
    )
    date = models.DateField(default=timezone.now)  # 仮のデフォルト値
    time = models.TimeField(default="00:00:00")  # 仮のデフォルト時間
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

    def __str__(self):
        return f"Participation by {self.user.username} on {self.created_at}"
