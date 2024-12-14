# api/factories/user_factory.py
import factory
from api.models.user_model import User

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    name = factory.Faker("name")  # ランダムな名前
    company = factory.Faker("company")  # ランダムな会社名
    birth_year = factory.Faker("random_int", min=1970, max=2005)  # 1970〜2005年のランダムな生年
    gender = factory.Iterator(["male", "female"])  # 男女ランダム
    department = factory.Iterator(
        ["sales", "planning", "general_affairs", "hr", "manufacturing", "development"]
    )
    joining_year = factory.Faker("random_int", min=2000, max=2023)  # ランダムな入社年
