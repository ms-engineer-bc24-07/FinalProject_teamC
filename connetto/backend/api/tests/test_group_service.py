# backend/api/tests/test_group_service.py
# グループ分けのロジック

import json
import random
from collections import defaultdict

from api.factories.participation_factory import ParticipationFactory
from api.factories.user_profile_factory import UserProfileFactory
from api.services.group_service import (
    assign_users_to_groups,
    group_users_by_date_and_preference,
)
from django.conf import settings  # settings.py のスコア設定をインポート
from django.test import TestCase


class GroupServiceTestCase(TestCase):
    def setUp(self):
        # テスト用データのセットアップ
        self.user_profiles = UserProfileFactory.create_batch(30)
        self.participations = ParticipationFactory.create_batch(30)

        # ユーザーとその参加データを関連付ける
        for user_profile, participation in zip(self.user_profiles, self.participations):
            desired_dates = (
                participation.desired_dates
                if isinstance(participation.desired_dates, str)
                else ", ".join(participation.desired_dates)
            )

            # 各属性のラベルをタプルの2番目の要素として取得
            gender_restriction = (
                participation.gender_restriction[1]
                if isinstance(participation.gender_restriction, tuple)
                else participation.gender_restriction
            )
            age_restriction = (
                participation.age_restriction[1]
                if isinstance(participation.age_restriction, tuple)
                else participation.age_restriction
            )
            joining_year_restriction = (
                participation.joining_year_restriction[1]
                if isinstance(participation.joining_year_restriction, tuple)
                else participation.joining_year_restriction
            )
            department_restriction = (
                participation.department_restriction[1]
                if isinstance(participation.department_restriction, tuple)
                else participation.department_restriction
            )
            atmosphere_preference = (
                participation.atmosphere_preference[1]
                if isinstance(participation.atmosphere_preference, tuple)
                else participation.atmosphere_preference
            )
            # ユーザーの参加データを更新
            user_profile.desired_dates = desired_dates
            user_profile.gender_restriction = gender_restriction
            user_profile.age_restriction = age_restriction
            user_profile.joining_year_restriction = joining_year_restriction
            user_profile.department_restriction = department_restriction
            user_profile.atmosphere_preference = atmosphere_preference
            user_profile.save()

    # ここからグループ分けスタート
    def test_group_users_by_date_and_preference(self):
        """
        ユーザーの飲み会希望日を基にグループ分けする関数。
        """
        participation = self.participations
        # preferences = ParticipationFactory.objects.all() # モックデータを使用

        # 希望日ごとにユーザーをグループ化
        grouped_by_date = defaultdict(list)

        for participation in self.participations:
            user = participation.user
            # 希望日でグループ化
            desired_dates = json.loads(participation.desired_dates)

            # 希望日が設定されていれば、その日付を使う
            if isinstance(desired_dates, list) and desired_dates:
                desired_date = desired_dates[0]  # 最初の希望日時を使用
                grouped_by_date[desired_date].append(participation)

        # グループ分けの途中経過を表示
        print("\n==== 希望日ごとのグループ分け ====")
        for date, participation_list in grouped_by_date.items():
            print(f"\n希望日: {date}")
            for participation in participation_list:
                user_profile = participation.user
                full_name = user_profile.full_name
                print(f"    ユーザー: {full_name}")

        # 希望日ごとに、スコアリングしてグループを作成
        final_groups = []

        for date, participations in grouped_by_date.items():
            scored_users = []

        for participation in participations:
            user = participation.user
            score = 0

            # 希望条件に基づいてスコアリング

            # 性別制限スコアリング
            if (
                participation.gender_restriction == "same_gender"
                and user.gender == participation.user.gender
            ):
                score += settings.SCORING_WEIGHTS["性別制限"]["同性"]
            else:
                score += settings.SCORING_WEIGHTS["性別制限"]["希望なし"]

            # 年代制限スコアリング
            if (
                participation.age_restriction == "same_age"
                and user.birth_year == participation.user.birth_year
            ):
                score += settings.SCORING_WEIGHTS["年代制限"]["同年代"]
            else:
                score += settings.SCORING_WEIGHTS["年代制限"]["希望なし"]

            # 部署制限スコアリング
            if (
                participation.department_restriction == "same_department"
                and user.department == participation.user.department
            ):
                score += settings.SCORING_WEIGHTS["部署希望"]["所属部署内希望"]
            else:
                score += settings.SCORING_WEIGHTS["部署希望"]["希望なし"]

            # お店の雰囲気制限スコアリング
            if (
                participation.atmosphere_preference == "calm"
                and user.shop_preference == "calm"
            ):
                score += settings.SCORING_WEIGHTS["お店の雰囲気"]["落ち着いたお店"]
            elif (
                participation.atmosphere_preference == "lively"
                and user.shop_preference == "lively"
            ):
                score += settings.SCORING_WEIGHTS["お店の雰囲気"]["わいわいできるお店"]
            else:
                score += settings.SCORING_WEIGHTS["お店の雰囲気"]["希望なし"]

            # 他の条件も追加可能...
            scored_users.append((user, score))

        # スコア順にソートし、3～6人のグループを作成
        scored_users.sort(key=lambda x: x[1], reverse=True)
        selected_group = scored_users[: random.randint(3, 6)]  # 3～6人をランダムで選出
        final_groups.append(
            [user[0] for user in selected_group]
        )  # ユーザーのみをグループに追加

        # スコアリング結果と選出されたグループを表示
        print("\n==== スコアリング結果 ====")
        for user, score in scored_users:
            print(f"ユーザー: {user.full_name}, スコア: {score}")

        print("\n==== 選出されたグループ ====")
        for user in selected_group:
            print(f"  {user[0].full_name} (スコア: {user[1]})")

        return final_groups


# def select_random_leader(group, excluded_leaders=[]):
#     """
#     グループ内からランダムに幹事を選出。
#     除外リストに全員が含まれる場合、除外ルールをリセットして選出する。
#     """
#     # 除外リストに含まれていないユーザーを幹事候補とする
#     potential_leaders = [user for user in group if user not in excluded_leaders]

#     # 幹事候補がいない場合は除外リストをリセットする
#     if not potential_leaders:
#         print("\n全員が幹事を経験済みのため、除外リストをリセットして再選出します")
#         potential_leaders = group  # 全員を候補に戻す
#         excluded_leaders.clear()  # 除外リストをリセット

#     # 幹事をランダムに選出
#     return random.choice(potential_leaders)


# def assign_users_to_groups():
#     """
#     グループ分けを実行し、幹事を各グループに割り当てる。
#     """
#     # グループ分けを実行
#     groups = group_users_by_date_and_preference()

#     # 幹事選出
#     group_leaders = {}
#     excluded_leaders = []  # 以前選出された幹事を除外

#     for i, group in enumerate(groups):
#         leader = select_random_leader(group, excluded_leaders)

#         # 幹事を選出し、結果を格納
#         group_leaders[f"Group {i + 1}"] = leader.name if leader else "No leader"

#         # 選出されたリーダーを除外リストに追加
#         if leader:
#             excluded_leaders.append(leader)  # 幹事選出後、履歴に追加

#         print(f"グループ {i + 1} の幹事は {leader.name} です")

#     return groups, group_leaders
