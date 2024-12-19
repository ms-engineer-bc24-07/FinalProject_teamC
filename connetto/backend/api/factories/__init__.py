# api/factories/__init__.py

from api.models.participation_model import Participation  # Participationをインポート

from .participation_factory import ParticipationFactory
from .user_profile_factory import UserProfileFactory

# UserProfile インスタンスを生成
user_profile = UserProfileFactory()

# Participation インスタンスを生成
participation = ParticipationFactory()

# ユーザー名とフルネームをそのまま表示
print(f"ユーザー名: {user_profile.username}")
print(f"フルネーム: {user_profile.full_name}")


# 選択肢のラベルを表示
def get_choice_label(choices, value):
    for val, label in choices:
        if val == value:
            return label
    return value  # 該当しない場合はそのまま返す


print(
    "性別制限:",
    get_choice_label(
        Participation._meta.get_field("gender_restriction").choices,
        participation.gender_restriction,
    ),
)
print(
    "年齢制限:",
    get_choice_label(
        Participation._meta.get_field("age_restriction").choices,
        participation.age_restriction,
    ),
)
print(
    "入社年制限:",
    get_choice_label(
        Participation._meta.get_field("joining_year_restriction").choices,
        participation.joining_year_restriction,
    ),
)
print(
    "部署制限:",
    get_choice_label(
        Participation._meta.get_field("department_restriction").choices,
        participation.department_restriction,
    ),
)
print(
    "雰囲気の好み:",
    get_choice_label(
        Participation._meta.get_field("atmosphere_preference").choices,
        participation.atmosphere_preference,
    ),
)

# 希望日程（そのまま表示）
print("希望日程:", participation.desired_dates)
