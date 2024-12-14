# api/factories/party_preference_factory.py
import factory
from api.models.party_preference_model import PartyPreference
from api.factories.user_factory import UserFactory

class PartyPreferenceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PartyPreference

    user = factory.SubFactory(UserFactory)  # 関連する User インスタンスを生成
    gender_restriction = factory.Iterator(["same_gender", "no_restriction"])
    age_restriction = factory.Iterator(["same_age", "broad_age", "no_restriction"])
    joining_year_restriction = factory.Iterator(["exact_match", "no_restriction"])
    department_restriction = factory.Iterator(
        ["same_department", "mixed_departments", "no_restriction"]
    )
    atmosphere_preference = factory.Iterator(["quiet", "lively", "no_restriction"])
    desired_date = factory.Faker("date")  # ランダムな日付
