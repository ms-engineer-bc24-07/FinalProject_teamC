from django.core.management.base import BaseCommand
from api.factories.user_factory import UserFactory
from api.factories.participation_factory import ParticipationFactory

class Command(BaseCommand):
    help = "Generate seed data for the application."

    def handle(self, *args, **kwargs):
        # 10件のユーザーを生成
        users = UserFactory.create_batch(10)

        # 各ユーザーに 3 件の Participation を生成
        for user in users:
            ParticipationFactory.create_batch(3, user=user)

        self.stdout.write(self.style.SUCCESS('Successfully generated seed data!'))
