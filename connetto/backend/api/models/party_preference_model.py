# このファイルは削除予定

# api/models/party_preference_model.py

from api.models.user_model import User
from django.db import models
from django.core.validators import MinValueValidator  # 追加
from datetime import datetime  # 追加

# 遅延インポート
def import_user_model():
    from api.models.user_model import User
    return User

class PartyPreference(models.Model):
    user = models.ForeignKey("api.User", on_delete=models.CASCADE)  # ユーザーID
    date = models.DateField()
    time = models.TimeField()
    venue_preference = models.CharField(max_length=50)
    gender_restriction = models.CharField(
        max_length=50, 
        choices=[("same_gender", "同性"), ("no_restriction", "希望なし")]
    )
    age_restriction = models.CharField(
        max_length=50,
        choices=[
            ("same_age", "同年代"),
            ("broad_age", "幅広い年代"),
            ("no_restriction", "希望なし"),
        ],
    )
    joining_year_restriction = models.CharField(
        max_length=50, 
        choices=[("exact_match", "完全一致"), ("no_restriction", "希望なし")]
    )
    department_restriction = models.CharField(
        max_length=50,
        choices=[
            ("same_department", "所属部署内希望"),
            ("mixed_departments", "他部署混在"),
            ("no_restriction", "希望なし"),
        ],
    )
    atmosphere_preference = models.CharField(
        max_length=50,
        choices=[
            ("quiet", "落ち着いたお店"),
            ("lively", "わいわいできるお店"),
            ("no_restriction", "希望なし"),
        ],
    )
    desired_date = models.DateField(
        validators=[MinValueValidator(datetime.today().date())]  # 今日以降の日付制限
    )  # 希望日

    def __str__(self):
        # 遅延インポートされたUserモデルを使う
        User = import_user_model()
        return f"Preference for {self.user.name} ({self.user.department})"
