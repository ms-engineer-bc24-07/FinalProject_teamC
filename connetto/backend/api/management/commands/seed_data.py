import random
from datetime import datetime, timedelta
from json import dumps

from api.factories.participation_factory import ParticipationFactory
from api.factories.user_profile_factory import UserProfileFactory
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Generate seed data for the application."

    def handle(self, *args, **kwargs):
        # 10件のユーザーを生成
        users = UserProfileFactory.create_batch(10)

        # 同じ日時で複数のユーザーを作成するための基準となる日時
        base_date = datetime.today()

        # 各ユーザーに関連するデータを生成
        for user in users:
            # Participationを1件生成
            for _ in range(1):
            # 同じ日時で希望日時を設定するため、ランダムに生成
                ParticipationFactory.create(user=user)

        self.stdout.write(
            self.style.SUCCESS("Successfully generated seed data for 10 users!")
        )
