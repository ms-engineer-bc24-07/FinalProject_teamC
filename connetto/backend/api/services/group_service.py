# backend/api/services/group_service.py
# グループ分けのロジック

import json #希望日時で絞り込み
import random
from collections import defaultdict #希望日時で絞り込み
from datetime import datetime, timedelta  # 日付操作のため

from api.models.group_member_model import GroupMember  # グループメンバーモデル
from api.models.group_model import Group  # Groupモデルをインポート（グループ作成に必要）
from api.models.participation_model import Participation  # Participationモデルをインポート
from api.models.user_profile_model import UserProfile  # Userモデルをインポート
from django.contrib.auth.models import User
from django.conf import settings  # settings.py のスコア設定をインポート


def group_users_by_date_and_preference():
    """
    ユーザーの希望日字を基にグループ分けする関数。
    希望日から3日前を過ぎた場合にグループ分けを開始する。
    """
    # 現在の日付を取得
    today = datetime.today()
    
    # 希望日から3日前を計算
    three_days_before = today - timedelta(days=3)

    # 現在日付が3日前を過ぎているかを確認
    if today >= three_days_before:
        print("グループ分けを開始します")
    else:
        print("まだグループ分けを開始できません")

    # 希望条件を取得
    participations = Participation.objects.all() # Participationモデルから全データを取得

    # 希望日時が正しく取得されているかを確認
    for participation in participations:
        desired_dates = participation.desired_dates
        print(f"ユーザー: {participation.user.full_name}, 希望日: {desired_dates}")

    # 希望日ごとにユーザーをグループ化
    grouped_by_date = defaultdict(list) # 希望日ごとにユーザーを格納するための辞書

    # 希望日時ごとにグループ化
    for participation in participations:
        desired_dates = participation.desired_dates  # 希望日時を取得
        
        # 希望日が設定されていれば、その日付を使う
        if isinstance(desired_dates, list) and desired_dates:
            # 希望日を一意にする
            unique_dates = list(set(desired_dates))  # 重複を排除

            # 各希望日時を処理
            for date_str in unique_dates:
                # 余計な空白を削除
                date_str = date_str.strip()  # 空白の削除

                # もし時間部分が含まれている場合、時間部分を切り取る
                if " " in date_str:
                    date_str = date_str.split(" ")[0]  # 時間を取り除く

                # 時間部分を含むフォーマットに対応
                try:
                    # 日付と時間を含むフォーマット
                    date = datetime.strptime(date_str, "%Y-%m-%d %H:%M") 
                except ValueError:
                    try:
                        # 時間部分がない場合
                        date = datetime.strptime(date_str, "%Y-%m-%d") 
                    except ValueError:
                        print(f"無効な日時形式: {date_str}")
                        continue  # 次の希望日時へ進む
                
                # 希望日が3日前を過ぎていればグループ分け
                if date <= three_days_before:
                    grouped_by_date[date.date()].append(participation)

        else:
            # 単一の希望日がある場合
            date_str = desired_dates.strip()
            if " " in date_str:
                date_str = date_str.split(" ")[0]  # 時間を取り除く

            try:
                date = datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                print(f"無効な日時形式: {date_str}")
                continue  # 次の参加者へ進む

            if date <= three_days_before:
                grouped_by_date[date.date()].append(participation)

    # グループ分けの途中経過を表示
    print("\n==== 希望日ごとのグループ分け ====")
    for date, participation_list in grouped_by_date.items():
        print(f"\n希望日: {date}")
        for participation in participation_list:
            user_profile = participation.user
            full_name = user_profile.full_name
            print(f"    ユーザー: {full_name}")

    # グループ分けされたデータが正しく格納されているか確認
    print("\n==== グループ分けされたデータ ====")
    for date, participation_list in grouped_by_date.items():
            print(f"\n希望日: {date}")
            user_names = [participation.user.full_name for participation in participation_list]
            print(f"    ユーザー: {', '.join(user_names)}")

    # 最終的に希望日ごとにグループ化されたデータを返す
    #return grouped_by_date

    final_groups = [] # 最終的なグループを格納するリスト

    # 最終的に希望日ごとにグループ化されたデータを返す前にグループ分けを行う
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
                    if participation1.age_restriction == "同年代":
                        # 生まれ年の差が4歳以内ならスコアを加算
                        if abs(user1.birth_year - user2.birth_year) <= 4:
                            score += settings.SCORING_WEIGHTS["年代制限"]["同年代"]
                    elif participation1.age_restriction == "幅広い年代":
                        score += settings.SCORING_WEIGHTS["年代制限"]["幅広い年代"]
                    else:
                        score += settings.SCORING_WEIGHTS["年代制限"]["希望なし"]

                # 入社年比較 
                if participation1.joining_year_restriction == participation2.joining_year_restriction:
                    if user1.join_year == user2.join_year:  # Profileモデルのjoin_yearを利用
                        score += settings.SCORING_WEIGHTS["入社年"]["完全一致"]
                else:
                    score += settings.SCORING_WEIGHTS["入社年"]["希望なし"]

                # 部署比較
                if participation1.department_restriction == participation2.department_restriction:
                    if user1.department == user2.department:
                        score += settings.SCORING_WEIGHTS["部署希望"]["所属部署内希望"]
                    elif participation1.department_restriction == "他部署混在":
                        score += settings.SCORING_WEIGHTS["部署希望"]["他部署混在"]
                    else:
                        score += settings.SCORING_WEIGHTS["部署希望"]["希望なし"]

                # お店の雰囲気比較
                if participation1.atmosphere_preference == participation2.atmosphere_preference:
                    if participation1.atmosphere_preference == participation2.atmosphere_preference:
                        # 雰囲気の好みが一致する場合にスコアを加算
                        score += settings.SCORING_WEIGHTS["お店の雰囲気"]["落ち着いたお店"]
                    elif participation1.atmosphere_preference == participation2.atmosphere_preference:
                        score += settings.SCORING_WEIGHTS["お店の雰囲気"]["わいわいできるお店"]
                    else:
                        # 希望なしの場合のスコアを加算
                        score += settings.SCORING_WEIGHTS["お店の雰囲気"]["希望なし"]

                # ペアごとのスコアを記録
                pair_scores.append(((user1, user2), score))

        # スコア順にソート
        pair_scores.sort(key=lambda x: x[1], reverse=True)

        # 上位のペアをグループに追加（最大6人まで）
        selected_users = set()
        for pair, _ in pair_scores:
            selected_users.update(pair)
            if len(selected_users) >= 6:
                break

        # ユーザーリストをグループとしてまとめる
        final_groups.append(list(selected_users))

        # スコアリング結果を表示
        print("\n==== ペアごとのスコアリング結果 ====")
        for (user1, user2), score in pair_scores:
            print(f"ペア: {user1.full_name} と {user2.full_name}, スコア: {score}")

        print("\n==== 選ばれたグループ ====")
        for user in selected_users:
            print(f"  {user.full_name}")

    return final_groups


def select_random_leader(group, excluded_leaders=[]):
    """
    グループ内からランダムに幹事を選出。
    除外リストに全員が含まれる場合、除外ルールをリセットして選出する。
    """
    # 除外リストに含まれていないユーザーを幹事候補とする
    potential_leaders = [user for user in group if user not in excluded_leaders]

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
        group_leaders[f"Group {i + 1}"] = leader.full_name if leader else "No leader"

        # 選出されたリーダーを除外リストに追加
        if leader:
            excluded_leaders.append(leader)  # 幹事選出後、履歴に追加

        print(f"グループ {i + 1} の幹事は {leader.full_name} です")

        # 希望日（desired_dates）をmeeting_dateとして保存
        participation = group[0].participations.first()  # 最初のparticipationを取得
        meeting_date = participation.desired_dates if group else None  
        # グループにメンバーがいれば、最初のメンバーの希望日を使用

        # データベースに保存する処理（save_groups_and_members）を呼び出し
        save_groups_and_members(groups, group_leaders, meeting_date)

    return groups, group_leaders

def save_groups_and_members(groups, group_leaders, meeting_date):
    """
    グループ分け結果をデータベースに保存し、各グループのメンバー情報も保存する。
    """
    # グループを保存
    for group_index, group_members in enumerate(groups):
        group_name = f"Group {group_index + 1}"
        
        # 幹事（リーダー）を特定
        leader_name = group_leaders.get(group_name)

        # リーダーのユーザーインスタンスを取得
        leader = User.objects.get(username=leader_name)

        # # リーダーの名前からUserインスタンスを取得
        # leader_profile = UserProfile.objects.filter(full_name=leader_name).first() if leader_name != "No leader" else None

        # # leader_profile が取得できれば、リーダーの UserProfile を取得
        # leader = leader_profile if leader_profile else None

        # if leader is None and leader_name != "No leader":
        #     print(f"リーダー '{leader_name}' が見つかりませんでした。")

        # グループを作成
        group = Group.objects.create(
            name=group_name,
            meeting_date=meeting_date,
            leader=leader
        )

        # グループにメンバーを追加
        for member in group_members:
            group_member = GroupMember.objects.create(
                group=group,
                user=member
            )
            group_member.save()

        group.save()
