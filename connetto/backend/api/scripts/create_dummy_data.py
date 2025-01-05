from api.models.user_profile_model import UserProfile
from api.models.participation_model import Participation
from django.contrib.auth.models import User
from random import choice, randint
from datetime import datetime, timedelta

def create_dummy_data():
    # ダミーデータ生成
    genders = ["male", "female"]
    departments = ["営業部", "人事部", "開発部", "マーケティング部"]
    stations = ["東京", "大井町", "横浜", "品川", "大崎"]
    desired_dates = ["2025-02-07T19:00:00Z"]

    for i in range(20):  # 30件作成
        # ユニークなユーザー名を作成
        username = f"dummy_user_{i}_{datetime.now().timestamp()}"
        # ユーザー作成
        user = User.objects.create_user(
            username=username,
            email=f"dummy_user_{i}@example.com",
            password="dummy_password"
        )
        print(f"ユーザー {user.username} を作成しました")

        # UserProfile 作成
        profile = UserProfile.objects.create(
            username=user.username,
            full_name=f"ダミー ユーザー{i}",
            furigana=f"ダミー ユーザー{i}",
            gender=choice(genders),
            birth_year=randint(1980, 2000),
            join_year=randint(2010, 2020),
            department=choice(departments),
            station=choice(stations),
        )
        print(f"UserProfile {profile.username} を作成しました")

        # Participation 作成
        participation = Participation.objects.create(
            user=user,
            gender_restriction=choice(["same_gender", "no_restriction"]),
            age_restriction=choice(["same_age", "broad_age", "no_restriction"]),
            joining_year_restriction=choice(["exact_match", "no_restriction"]),
            department_restriction=choice(["same_department", "mixed_departments", "no_restriction"]),
            atmosphere_preference=choice(["quiet", "lively", "no_restriction"]),
            desired_dates=[choice(desired_dates) for _ in range(randint(1, 3))]
        )
        print(f"Participation for {user.username} を作成しました")

    print("ダミーデータの作成が完了しました")

# 関数を呼び出し
create_dummy_data()

