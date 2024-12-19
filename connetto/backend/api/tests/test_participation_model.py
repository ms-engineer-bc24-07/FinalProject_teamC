# backend/api/tests/test_participation_model.py

from datetime import date, time

from api.models import Participation, UserProfile
from django.test import TestCase


class ParticipationModelTest(TestCase):
    def setUp(self):
        # テスト用の User インスタンスを作成
        self.user = UserProfile.objects.create(
            username="testuser",
            full_name="Test User",
            furigana="テスト ユーザー",
            gender="male",
            birth_year=1990,
            join_year=2020,
            department="sales",
            station="Tokyo",
            email="testuser@example.com",
        )

    def test_participation_save(self):
        # Participation インスタンスを作成
        participation = Participation.objects.create(
            user=self.user,
            desired_dates=[{"date": "2024-12-25", "time": "18:00:00"}],
        )
        # インスタンスの date と time が desired_dates の値に同期されているか確認
        self.assertEqual(participation.date, date(2024, 12, 25))
        self.assertEqual(participation.time, time(18, 0))
