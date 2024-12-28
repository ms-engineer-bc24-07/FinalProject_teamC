# backend/api/services/group_service.py
# グループ分けのロジック

import json
import random
from collections import defaultdict

from api.models.group_member_model import GroupMember  # グループメンバーモデル
from api.models.group_model import Group  # Groupモデルをインポート（グループ作成に必要）
from api.models.participation_model import Participation  # Participationモデルをインポート
from api.models.user_profile_model import UserProfile  # Userモデルをインポート
from django.conf import settings  # settings.py のスコア設定をインポート


def group_users_by_date_and_preference():
    """
    ユーザーの飲み会希望日を基にグループ分けする関数。
    """
    # ユーザーの飲み会希望日を基にグループ分け
    user = UserProfile.objects.all()  # User モデルから直接ユーザー情報を取得
    participations = Participation.objects.all()

    # 希望日ごとにユーザーをグループ化
    grouped_by_date = defaultdict(list)

    for participation in participations:
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

    # 希望日ごとにグループを作成
    final_groups = []

    for date, participations in grouped_by_date.items():
        pair_scores = []

        # 2人ずつ比較してスコアを計算
        for i, participation1 in enumerate(participations):
            user1 = participation1.user
            for j, participation2 in enumerate(participations):
                if i >= j:
                    continue  # 同じユーザー同士の比較はしない

                user2 = participation2.user
                score = 0

                # 性別比較
                if participation1.gender_restriction == participation2.gender_restriction:
                    if user1.gender == user2.gender:
                        score += settings.SCORING_WEIGHTS["性別制限"]["同性"]
                    else:
                        score += settings.SCORING_WEIGHTS["性別制限"]["希望なし"]

                # 年代比較
                if participation1.age_restriction == participation2.age_restriction:
                    if user1.birth_year == user2.birth_year:
                        score += settings.SCORING_WEIGHTS["年代制限"]["同年代"]
                    else:
                        score += settings.SCORING_WEIGHTS["年代制限"]["希望なし"]

                # 部署比較
                if participation1.department_restriction == participation2.department_restriction:
                    if user1.department == user2.department:
                        score += settings.SCORING_WEIGHTS["部署希望"]["所属部署内希望"]
                    else:
                        score += settings.SCORING_WEIGHTS["部署希望"]["希望なし"]

                # お店の雰囲気比較
                if participation1.shop_atmosphere_restriction == participation2.shop_atmosphere_restriction:
                    if user1.shop_preference == user2.shop_preference:
                        score += settings.SCORING_WEIGHTS["お店の雰囲気"]["一致"]
                    else:
                        score += settings.SCORING_WEIGHTS["お店の雰囲気"]["希望なし"]

                # 他の希望条件があれば、ここで追加

                # ペアごとのスコアを記録
                pair_scores.append(((user1, user2), score))

        # スコア順にソート
        pair_scores.sort(key=lambda x: x[1], reverse=True)

        # 上位のペアをグループに追加（最大6人まで）
        selected_pairs = pair_scores[:random.randint(3, 6)]
        selected_users = set()
        for pair, _ in selected_pairs:
            selected_users.update(pair)

        # ユーザーリストをグループとしてまとめる
        final_groups.append(list(selected_users))

        # スコアリング結果を表示
        print("\n==== ペアごとのスコアリング結果 ====")
        for (user1, user2), score in pair_scores:
            print(f"ペア: {user1.name} と {user2.name}, スコア: {score}")

        print("\n==== 選ばれたグループ ====")
        for user in selected_users:
            print(f"  {user.name}")

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
        leader = select_random_leader(group, excluded_leaders)

        # 幹事を選出し、結果を格納
        group_leaders[f"Group {i + 1}"] = leader.name if leader else "No leader"

        # 選出されたリーダーを除外リストに追加
        if leader:
            excluded_leaders.append(leader)  # 幹事選出後、履歴に追加

        print(f"グループ {i + 1} の幹事は {leader.name} です")

    return groups, group_leaders
