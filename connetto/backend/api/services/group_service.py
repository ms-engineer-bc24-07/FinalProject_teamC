# backend/api/services/group_service.py
# グループ分けのロジック

import random
from collections import defaultdict

from api.models.party_preference_model import PartyPreference

# from api.models.user_model import User  # Userモデルをインポート
from django.conf import settings  # settings.py のスコア設定をインポート


def group_users_by_date_and_preference():
    # ユーザーの飲み会希望日を基にグループ分け
    preferences = PartyPreference.objects.all()

    # 希望日ごとにユーザーをグループ化、企業ごとのサブグループを作成
    grouped_by_date_and_company = defaultdict(lambda: defaultdict(list))

    for preference in preferences:
        user = preference.user
        # ユーザーが所属する企業と希望日でグループ化
        grouped_by_date_and_company[preference.desired_date][user.company].append(
            preference
        )

    # 希望日ごとに、スコアリングしてグループを作成
    final_groups = []

    for date, preferences in grouped_by_date_and_company.items():
        scored_users = []

        for preference in preferences:
            user = preference.user
            score = 0

            # 希望条件に基づいてスコアリング

            # 性別制限スコアリング
            if (
                preference.gender_restriction == "same_gender"
                and user.gender == preference.user.gender
            ):
                score += settings.SCORING_WEIGHTS["性別制限"]["同性"]
            else:
                score += settings.SCORING_WEIGHTS["性別制限"]["希望なし"]

            # 年代制限スコアリング
            if (
                preference.age_restriction == "same_age"
                and user.birth_year == preference.user.birth_year
            ):
                score += settings.SCORING_WEIGHTS["年代制限"]["同年代"]
            else:
                score += settings.SCORING_WEIGHTS["年代制限"]["希望なし"]

            # 部署制限スコアリング
            if (
                preference.department_restriction == "same_department"
                and user.department == preference.user.department
            ):
                score += settings.SCORING_WEIGHTS["部署希望"]["所属部署内希望"]
            else:
                score += settings.SCORING_WEIGHTS["部署希望"]["希望なし"]

            # 他の条件も追加可能...
            scored_users.append((user, score))

        # スコア順にソートし、3～6人のグループを作成
        scored_users.sort(key=lambda x: x[1], reverse=True)
        selected_group = scored_users[: random.randint(3, 6)]  # 3～6人をランダムで選出
        final_groups.append(
            [user[0] for user in selected_group]
        )  # ユーザーのみをグループに追加

    return final_groups


def select_random_leader(group, excluded_leaders=[]):
    # 既に幹事になったユーザーを除外してランダムに選出
    potential_leaders = [(user for user in group if user not in excluded_leaders)]
    return random.choice(potential_leaders) if potential_leaders else None


def assign_users_to_groups():
    # グループ分けを実行
    groups = group_users_by_date_and_preference()

    # 幹事選出
    group_leaders = {}
    excluded_leaders = []  # 以前選出された幹事を除外
    for i, group in enumerate(groups):
        leader = select_random_leader(group, excluded_leaders)
        group_leaders[f"Group {i + 1}"] = leader.name if leader else "No leader"
        if leader:
            excluded_leaders.append(leader)  # 幹事選出後、履歴に追加

    return groups, group_leaders
