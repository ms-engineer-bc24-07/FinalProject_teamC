from django.core.management.base import BaseCommand
from api.factories.user_factory import UserFactory
from api.factories.participation_factory import ParticipationFactory
from api.factories.party_preference_factory import PartyPreferenceFactory
from api.factories.user_profile_factory import UserProfileFactory
from datetime import timedelta
import random

class Command(BaseCommand):
    help = "Generate seed data for the application."

    def handle(self, *args, **kwargs):
        # 50件のユーザーを同じ会社"connettoCompany"で生成
        users = UserFactory.create_batch(50, company="connettoCompany")

        # 同じ日時で複数のユーザーを作成するための基準となる日時
        base_date = datetime.today()

        # 各ユーザーに関連するデータを生成
        for user in users:
            # Participationを3件生成
            # 同じ日時で希望日時を設定するため、ランダムに生成
            desired_date = base_date + timedelta(days=random.randint(0, 5))  # 日時をランダムに決定
            ParticipationFactory.create_batch(3, user=user, desired_dates=[desired_date])

            # PartyPreferenceを1件生成
            PartyPreferenceFactory.create(user=user)

            # UserProfileを1件生成
            UserProfileFactory.create(user=user)

        self.stdout.write(self.style.SUCCESS('Successfully generated seed data for 50 users!'))
