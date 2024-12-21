# api/factories/user_profile_factory.py
import factory
from api.models.user_profile_model import UserProfile
from faker import Faker

faker = Faker(locale="ja_JP")  # 日本語データを生成する場合


class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    username = factory.Faker("user_name", locale="ja_JP")
    full_name = factory.Faker("name", locale="ja_JP")
    # furigana = factory.Faker("name")  # フリガナ生成
    gender = factory.Iterator(["男性", "女性"])
    birth_year = factory.Faker("random_int", min=1970, max=2005)
    join_year = factory.Faker("random_int", min=2000, max=2023)
    department = factory.Iterator(["営業", "企画", "総務", "人事"])
    station = factory.Iterator(["新宿", "渋谷", "池袋", "東京", "品川"])
    # station = factory.Faker("city", locale="ja_JP")
    # email = factory.LazyAttribute(lambda o: f"user{fake.random_number(digits=5)}@example.com")  # ユニークなemailを生成

    # @classmethod
    # def _create(cls, model_class, *args, **kwargs):
    #     return super()._create(model_class, *args, **kwargs)
