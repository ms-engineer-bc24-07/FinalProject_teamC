from django.db import models
from django.contrib.auth.models import User  # Djangoのデフォルトユーザーモデルを使用

class Participation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="participations")
    gender_restriction = models.CharField(
        max_length=50,
        choices=[
            ("same_gender", "同性"),
            ("no_restriction", "希望なし")
        ],
        default="no_restriction"
    )
    age_restriction = models.CharField(
        max_length=50,
        choices=[
            ("same_age", "同年代"),
            ("broad_age", "幅広い年代"),
            ("no_restriction", "希望なし"),
        ],
        default="no_restriction"
    )
    joining_year_restriction = models.CharField(
        max_length=50,
        choices=[
            ("exact_match", "同期のみ"), 
            ("no_restriction", "希望なし")
        ],
        default="no_restriction"
    )
    department_restriction = models.CharField(
        max_length=50,
        choices=[
            ("same_department", "所属部署内希望"),
            ("mixed_departments", "他部署混在"),
            ("no_restriction", "希望なし"),
        ],
        default="no_restriction"
    )
    atmosphere_preference = models.CharField(
        max_length=50,
        choices=[
            ("quiet", "落ち着いたお店"),
            ("lively", "わいわいできるお店"),
            ("no_restriction", "希望なし"),
        ],
        default="no_restriction"
    )
    desired_dates = models.JSONField()  # 希望日時をリスト形式で保存可能
    created_at = models.DateTimeField(auto_now_add=True)  # 登録日時
    updated_at = models.DateTimeField(auto_now=True)  # 更新日時

    def __str__(self):
        return f"Participation by {self.user.username} on {self.created_at}"
