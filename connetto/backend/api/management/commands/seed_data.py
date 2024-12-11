from api.models.user_model import User
from api.models.party_preference_model import PartyPreference  # PartyPreference をインポート
from django.utils.dateparse import parse_datetime
from datetime import datetime

def seed_data():
    data = [
        {
            "name": "田中圭",
            "email": "tanaka.kei@example.com",
            "birthYear": 1984,
            "gender": "男性",
            "department": "営業部",
            "joinYear": 2010,
            "nearestStation": "渋谷駅",
            "registrationDate": "2024-12-01T10:00:00",
            "partyRegistration": {
                "date": "2024-12-05",
                "time": "18:00",
                "genderRestriction": "同性",
                "ageRestriction": "同年代",
                "joinYear": "希望なし",
                "departmentPreference": "所属部署内希望",
                "atmosphere": "落ち着いたお店"
            }
        },
        # 他のデータ省略
    ]

    for entry in data:
        try:
            # PartyPreferenceを作成
            party_pref = PartyPreference.objects.create(
                user=None,  # User をまだ作成していないため一時的に None に設定
                gender_restriction=entry["partyRegistration"]["genderRestriction"],
                age_restriction=entry["partyRegistration"]["ageRestriction"],
                joining_year_restriction=entry["partyRegistration"]["joinYear"],
                department_restriction=entry["partyRegistration"]["departmentPreference"],
                atmosphere_preference=entry["partyRegistration"]["atmosphere"],
                desired_date=parse_datetime(entry["partyRegistration"]["date"] + "T" + entry["partyRegistration"]["time"])
            )

            # Userを作成
            user = User.objects.create(
                name=entry["name"],
                email=entry["email"],
                birth_year=entry["birthYear"],
                gender=entry["gender"],
                department=entry["department"],
                joining_year=entry["joinYear"],
                nearest_station=entry["nearestStation"],
                registration_date=parse_datetime(entry["registrationDate"]),
            )

            # PartyPreference にユーザーを紐付け
            party_pref.user = user
            party_pref.save()

            print(f"User {entry['name']} と PartyPreference の関連付けが完了しました")

        except Exception as e:
            print(f"データ挿入時にエラーが発生しました: {str(e)}")

    print("シーディングが完了しました")

# 実行
if __name__ == "__main__":
    seed_data()
