# backend/api/services/group_service.py
# グループ分けのロジック

import json #希望日時で絞り込み
import random
from collections import defaultdict #希望日時で絞り込み
from datetime import datetime, timedelta, date  # 日付操作のため
from django.db import models

from api.models.group_member_model import GroupMember  # グループメンバーモデル
from api.models.group_model import Group  # Groupモデルをインポート（グループ作成に必要）
from api.models.participation_model import Participation  # Participationモデルをインポート
from api.models.user_profile_model import UserProfile  # Userモデルをインポート
from django.contrib.auth.models import User
from django.conf import settings  # settings.py のスコア設定をインポート


def group_users_by_date_and_preference():
    """
    ユーザーの希望日時を基にグループ分け、meeting_date を設定する関数。
    希望日から3日前を過ぎた場合にグループ分けを開始する。
    時間誤差1時間以内なら同じグループにする。
    複数の希望日時がある場合は第1希望を優先、第2希望を使用する。
    
    """
  
    today = datetime.today()  # 現在の日付を取得  
    three_days_before = today - timedelta(days=3) # 希望日から3日前を計算

    # 現在日付が3日前を過ぎているかを確認
    if today >= three_days_before:
        print("グループ分けを開始します")
    else:
        print("まだグループ分けを開始できません")

    # 希望日時ごとにユーザーをグループ化
    grouped_by_date = defaultdict(list) 
    assigned_users = set()  # 割り当て済みのユーザーを追跡

    # 希望条件を取得
    participations = Participation.objects.all() # Participationモデルから全データを取得

    # 希望日時が正しく取得されているかを確認
    for participation in participations:
        desired_dates = participation.desired_dates
        print(f"ユーザー: {participation.user.full_name}, 希望日: {desired_dates}")

        # 希望日がリストの場合
        if isinstance(desired_dates, list) and desired_dates:
            # 最初の希望日時を基準に
            for i, date_str in enumerate(desired_dates):
                # 日付文字列をパース
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%d %H:%M") 
                except ValueError:
                    continue  # 無効な日時形式はスキップ

                # ユーザーがすでに割り当てられている場合はスキップ
                if participation.user.full_name in assigned_users:
                    print(f"{participation.user.full_name} はすでにグループに割り当て済みです。")
                    break

                # もし希望日時に合う他のユーザーがいれば、同じグループに
                grouped = False
                for group_date, group in grouped_by_date.items():
                    # 既存グループの日時と1時間以内であれば同じグループにする
                    if abs((date - group_date).total_seconds()) <= 3600:  # 1時間以内
                        if participation not in group:  # 重複確認
                            group.append(participation)
                            assigned_users.add(participation.user.full_name)  # 割り当て済みに追加
                        grouped = True
                        break  # グループ分けができたら次の日時へ

                # 希望日時に合うグループがなければ新しいグループを作成
                if not grouped:
                    grouped_by_date[date].append(participation)
                    assigned_users.add(participation.user.full_name)  # 割り当て済みに追加

                # 第1希望が処理された場合は終了
                if i == 0 and grouped:
                    break

        else:
            # 単一の希望日時の場合
            date_str = desired_dates.strip()
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")  # 時間あり
            except ValueError:
                continue

            # グループ分け
            grouped = False
            for group_date, group in grouped_by_date.items():
                if abs((date - group_date).total_seconds()) <= 3600:  # 1時間以内
                    if participation not in group:  # 重複確認
                        group.append(participation)
                    grouped = True
                    break

            if not grouped:
                grouped_by_date[date].append(participation)

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
    #return grouped_by_date, assigned_users

    final_groups = [] # 最終的なグループを格納するリスト

    # 最終的に希望日ごとにグループ化されたデータを返す前にグループ分けを行う
    for date, participations in grouped_by_date.items():
        # グループ化された日時をmeeting_dateとする
        meeting_date = date

        # 希望条件に基づくスコアリングを実施
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
        final_groups.append({
            "meeting_date": meeting_date,
            "users": list(selected_users)
    })

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

def generate_unique_group_name(base_name):
    """
    与えられたグループ名がすでに存在する場合、ユニークな名前を生成する。
    """
    import re
    from django.db.models import IntegerField, Max

    # グループ名の末尾に付けられた番号を正規表現で抽出する
    number_pattern = re.compile(r'(\d+)$')
    
    # すべてのグループ名を取得
    group_names = Group.objects.values_list('name', flat=True)

    # 最大番号を抽出
    max_group_number = 0
    for name in group_names:
        match = number_pattern.search(name)
        if match:
            number = int(match.group(1))
            max_group_number = max(max_group_number, number)
    
    # 新しい番号を計算
    group_number = max_group_number + 1
    unique_name = f"{base_name} {group_number}"

    # ユニーク性を確認しながら名前を生成
    while Group.objects.filter(name=unique_name).exists():
        group_number += 1
        unique_name = f"{base_name} {group_number}"

    return unique_name 

def assign_users_to_groups():
    """
    グループ分けを実行し、幹事を各グループに割り当てる。
    """
    # グループ分けを実行
    groups = group_users_by_date_and_preference()

    # 幹事選出
    leaders = {}
    excluded_leaders = []  # 以前選出された幹事を除外

    for group_index, group in enumerate(groups, start=1):
        users = group['users']

        # 幹事をランダムに選出
        selected_leader = select_random_leader(users, excluded_leaders)

        # ユニークなグループ名を生成
        base_name = generate_unique_group_name(f"Group {group_index}")  
        group['name'] = base_name  # ここでユニークなグループ名を設定

        # 幹事を選出し、結果を格納
        if isinstance(selected_leader, str):
            leaders[base_name] = selected_leader
        else:
            leaders[base_name] = selected_leader.full_name if selected_leader else "No leader"

        print(f"グループ {base_name} の幹事は {selected_leader.full_name} です")

        # 選出されたリーダーを除外リストに追加
        if selected_leader:
            excluded_leaders.append(selected_leader)  # 幹事選出後、履歴に追加

        # グループに割り当てられた日時を決定
        # group_users_by_date_and_preference() で既に希望日時が決まっているので、そのまま使用
        meeting_date= group['meeting_date'] 

        # データベースに保存する処理（save_groups_and_members）を呼び出し
        save_groups_and_members(groups, leaders, meeting_date)

    return groups, leaders

def save_groups_and_members(groups, leaders, meeting_date):
    """
    グループ分け結果をデータベースに保存し、各グループのメンバー情報も保存する。
    """

    # グループを保存
    for group_index, group in enumerate(groups):
        group_name =  f"Group {group_index + 1}"

        # グループ名の重複チェック
        if Group.objects.filter(name=group_name).exists():
            print(f"グループ名 '{group_name}' は既に存在します。")
            continue  # 重複があれば次のグループに進む
        
        # 幹事（リーダー）を特定
        leader_name = leaders.get(group_name)

        # リーダーの名前からUserインスタンスを取得
        leader_profile = UserProfile.objects.filter(full_name=leader_name).first() 

        # リーダーのUserProfileが存在すれば、リーダーのユーザーを取得
        if leader_profile:
            try:
                leader = leader_profile.user  # UserProfile から関連する User を取得
            except AttributeError:
                print(f"リーダー '{leader_name}' に関連する User が見つかりませんでした。")
                leader = None
        else:
            print(f"リーダー '{leader_name}' に対応するUserProfileが見つかりませんでした。")
            leader = None

        # 幹事の重複チェック
        if leader and Group.objects.filter(leader=leader).exists():
            print(f"幹事 '{leader_name}' は既に他のグループに割り当てられています。")
            continue  # 重複があれば次のグループに進む

        meeting_date= group['meeting_date'] 
        # meeting_date がリストでないことを確認
        if not isinstance(meeting_date, str):
                print(f"meeting_date は日付型でないため、保存できません: {meeting_date}")
                continue        

        # グループを作成し、「確定した日時」を保存
        group = Group.objects.create(
            name=group_name,
            meeting_date=meeting_date,
            leader=leader # leader_profileをそのまま使用
        )

        # グループにメンバーを追加
        for member in group['users']:
            # member は UserProfile 型なので、UserProfile から User を取得
            try:
                user = member.user  # UserProfile から関連する User を取得

                # メンバーの重複チェック
                if GroupMember.objects.filter(group=group, user=user).exists():
                    print(f"メンバー '{user.username}' はグループ '{group_name}' に既に追加されています。")
                    continue  # 重複があれば次のメンバーに進む

                # グループメンバーを作成
                GroupMember.objects.create(
                    group=group,
                    user=user
                )
            except User.DoesNotExist:
                print(f"メンバー '{member.username}' に対応するUserが見つかりませんでした。")


