# api/factories/participation_factory.py
import datetime
import json
import random

import factory
from api.factories.user_profile_factory import UserProfileFactory
from api.models.participation_model import Participation
from faker import Faker

# from datetime import datetime, timedelta

fake = Faker(locale="ja_JP")  # 日本語ロケールのFaker


class ParticipationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Participation

    user = factory.SubFactory(UserProfileFactory)  # 関連する User インスタンスを生成

    # 性別制限
    gender_restriction = factory.Iterator(
        [("same_gender", "同性"), ("no_restriction", "希望なし")]
    )

    # 年齢制限
    age_restriction = factory.Iterator(
        [
            ("same_age", "同年代"),
            ("broad_age", "幅広い年代"),
            ("no_restriction", "希望なし"),
        ]
    )

    # 入社年制限
    joining_year_restriction = factory.Iterator(
        [("exact_match", "同期のみ"), ("no_restriction", "希望なし")]
    )

    # 部署制限
    department_restriction = factory.Iterator(
        [
            ("same_department", "所属部署内希望"),
            ("mixed_departments", "他部署混在"),
            ("no_restriction", "希望なし"),
        ]
    )

    # 雰囲気の好み
    atmosphere_preference = factory.Iterator(
        [
            ("quiet", "落ち着いたお店"),
            ("lively", "わいわいできるお店"),
            ("no_restriction", "希望なし"),
        ]
    )

    # 希望日程
    desired_dates = factory.LazyAttribute(
        lambda o: json.dumps(
            [
                f"{str(fake.date_between(start_date=datetime.date(2024, 12, 1), end_date=datetime.date(2024, 12, 5)))} "
                f"{random.choice(['18:30', '19:00', '19:30', '20:00', '20:30', '21:00'])}"
            ]
        )
    )
