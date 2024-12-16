# backend/api/services/group_service.py
# グループ分けのロジック

import random
from collections import defaultdict

from api.models.group_model import Group  # Groupモデルをインポート（グループ作成に必要）
from api.models.participation_model import Participation  # participationモデルをインポート
from api.models.user_profile_model import UserProfile  # Userモデルをインポート
from django.conf import settings  # settings.py のスコア設定をインポート


def group_users_by_date_and_preference():
    """
    ユーザーの飲み会希望日を基にグループ分けする関数。
    """
    # ユーザーの飲み会希望日を基にグループ分け
    user = UserProfile.objects.all()  # User モデルから直接ユーザー情報を取得
    preferences = Participation.objects.all()

    # 希望日ごとにユーザーをグループ化、企業ごとのサブグループを作成
    grouped_by_date_and_company = defaultdict(lambda: defaultdict(list))

    for preference in preferences:
        user = preference.user
        # ユーザーが所属する企業と希望日でグループ化
        grouped_by_date_and_company[preference.desired_date][user.company].append(
            preference
        )

    # グループ分けの途中経過を表示
    print("\n==== 希望日と企業ごとのグループ分け ====")
    for date, company_groups in grouped_by_date_and_company.items():
        print(f"\n希望日: {date}")
        for company, preferences in company_groups.items():
            print(f"  企業: {company}")
            for preference in preferences:
                print(f"    ユーザー: {preference.user.name}")

    # 希望日ごとに、スコアリングしてグループを作成
    final_groups = []

    for date, company_groups in grouped_by_date_and_company.items():
        scored_users = []

        for company, preferences in company_groups.items():
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

            # お店の雰囲気制限スコアリング
            if (
                preference.shop_atmosphere_restriction == "calm"
                and user.shop_preference == "calm"
            ):
                score += settings.SCORING_WEIGHTS["お店の雰囲気"]["落ち着いたお店"]
            elif (
                preference.shop_atmosphere_restriction == "lively"
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
            print(f"ユーザー: {user.name}, スコア: {score}")

        print("\n==== 選出されたグループ ====")
        for user in selected_group:
            print(f"  {user[0].name} (スコア: {user[1]})")

    return final_groups


def select_random_leader(group, excluded_leaders=[]):
    """
    グループ内からランダムに幹事を選出。
    除外リストに全員が含まれる場合、除外ルールをリセットして選出する。
    """
    # 除外リストに含まれていないユーザーを幹事候補とする
    potential_leaders = [(user for user in group if user not in excluded_leaders)]

    # 幹事候補がいない場合は除外リストをリセットする
    if not potential_leaders:
        print("\n全員が幹事を経験済みのため、除外リストをリセットして再選出します")
        potential_leaders = group  # 全員を候補に戻す
        excluded_leaders.clear()  # 除外リストをリセット

    # 幹事をランダムに選出
    return random.choice(potential_leaders)


def assign_users_to_groups():
    """
    グループ分けを実行し、幹事を各グループに割り当てる。
    """
    # グループ分けを実行
    groups = group_users_by_date_and_preference()

    # 幹事選出
    group_leaders = {}
    excluded_leaders = []  # 以前選出された幹事を除外

    for i, group in enumerate(groups):
        # 幹事を選出
        leader = select_random_leader(group, excluded_leaders)

        # グループ情報をデータベースに保存
        group_model = Group.objects.create(
            name=f"Group_{i + 1}",
            meeting_date=group[0].participation.date,  # グループの希望日を設定
            leader=leader,
        )
        group_model.members.set(group)  # グループのメンバーを設定
        group_model.save()

        # 幹事を選出し、結果を格納
        group_leaders[f"Group {i + 1}"] = leader.name if leader else "No leader"

        # 選出されたリーダーを除外リストに追加
        if leader:
            excluded_leaders.append(leader)  # 幹事選出後、履歴に追加

        print(f"グループ {group_model.name} の幹事は {leader.username} です")

    return groups, group_leaders
