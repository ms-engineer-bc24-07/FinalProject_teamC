# api/models/user_profile_model.py

from django.core.management.base import BaseCommand
from api.models import UserProfile  # ここでインポート

# 以下はそのまま
def import_factories():
    from api.factories.user_factory import UserFactory
    from api.factories.participation_factory import ParticipationFactory
    from api.factories.party_preference_factory import PartyPreferenceFactory
    from api.factories.user_profile_factory import UserProfileFactory
    return UserFactory, ParticipationFactory, PartyPreferenceFactory, UserProfileFactory

class Command(BaseCommand):
    help = "Generate seed data for the application."

    def handle(self, *args, **kwargs):
        UserFactory, ParticipationFactory, PartyPreferenceFactory, UserProfileFactory = import_factories()

        try:
            users = UserFactory.create_batch(10)
            for user in users:
                ParticipationFactory.create_batch(3, user=user)
                PartyPreferenceFactory.create(user=user)
                user_profile = UserProfileFactory.create(user=user)
                self.stdout.write(self.style.SUCCESS(f'Generated UserProfile for {user.username}'))

            self.stdout.write(self.style.SUCCESS('Successfully generated seed data!'))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error occurred: {e}'))
