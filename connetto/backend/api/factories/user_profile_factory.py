# api/factories/user_profile_factory.py
import factory
from api.models.user_profile_model import UserProfile

class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    username = factory.Faker("user_name")
    full_name = factory.Faker("name")
    furigana = factory.Faker("name", locale="ja_JP")  # 日本語名（フリガナ）
    gender = factory.Iterator(["male", "female"])
    birth_year = factory.Faker("random_int", min=1970, max=2005)
    join_year = factory.Faker("random_int", min=2000, max=2023)
    department = factory.Iterator(["sales", "planning", "general_affairs", "hr"])
    station = factory.Faker("city")
