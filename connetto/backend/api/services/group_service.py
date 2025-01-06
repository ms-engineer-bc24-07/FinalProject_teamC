import random
import openai
import os
from dotenv import load_dotenv
from collections import defaultdict
from datetime import datetime
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import User
from api.models.group_member_model import GroupMember
from api.models.group_model import Group
from api.models.user_profile_model import UserProfile
from api.models.participation_model import Participation
from api.models.notification_model import Notification, NotificationType
from api.services.venue_service import VenueService
from datetime import datetime, timezone

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_midpoint_station(stations):
    """
    ChatGPTを使用して、複数の駅の中間地点となる駅を取得する関数。
    """
    try:

        prompt = (
        f"以下の駅リストがあります:\n{', '.join(stations)}\n"
        f"これらの駅の飲み会に最適な中間地点となる駅を1つ提案してください。"
        f"答えは駅名のみで、余分な説明は不要です。"
    )
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ]
        )

        message_content = response.choices[0].message.content

        return message_content


    except Exception as e:  # すべてのエラーをキャッチ
        print(f"エラーが発生しました: {e}")
    

def group_users_by_date_and_preference():
    """
    ユーザーの希望日時を基にグループ分けし、希望条件ごとのスコアリングを行う。
    """
    grouped_by_date = defaultdict(list)

    # 対象の日付を指定
    target_date = "2025-01-31T19:00:00Z"
    participations = Participation.objects.filter(desired_dates__contains=[target_date])

    print(f"[DEBUG] 取得した参加者の総数: {len(participations)}")

    # 希望日時ごとに参加者をグループ化
    grouped_by_date[target_date] = list(participations)

    # デバッグ: grouped_by_date の内容を確認
    #print(f"[DEBUG] Grouped by date: {grouped_by_date}")

    final_groups = []

    for meeting_date, participations in grouped_by_date.items():
        # ペアのスコアを計算
        pair_scores = []
        for i, participation1 in enumerate(participations):
            user1 = participation1.user
            for j, participation2 in enumerate(participations):
                if i >= j:
                    continue
                user2 = participation2.user
                score = calculate_pair_score(participation1, participation2, user1, user2)
                
                # 希望条件がないペアもスコア0でリストに含める
                if score is None:
                    score = 0
                
                # ペアとスコアが正しい形式であるかを確認
                if user1 and user2:
                    if isinstance(score, (int, float)):
                        pair_scores.append(((user1, user2), score))
                    else:
                        print(f"[ERROR] Invalid score type: {score} (Type: {type(score)})")
                else:
                    print(f"[ERROR] Invalid users: user1={user1}, user2={user2}")

        # スコア順に並べ替え
        pair_scores.sort(key=lambda x: x[1], reverse=True)

        
        # デバッグログ: pair_scores の内容を確認
        #print(f"[DEBUG] Pair scores: {pair_scores}")

        if not pair_scores:
            print("[DEBUG] No valid pair_scores. Skipping this date.")
            continue

        # ユーザーリストを初期化
        remaining_users = set(p.user for p in participations)

        while remaining_users:
            # 残りユーザー数に基づいてグループサイズを設定
            group_size = min(len(remaining_users), random.choice([3, 4, 5, 6]))

            current_group = set()

            print(f"[DEBUG] Processing pair_scores: {pair_scores}")

            for pair_score in pair_scores:
                #print(f"[DEBUG] Pair score entry: {pair_score}")
                # pair_score のフォーマットが正しいかチェック
                if not isinstance(pair_score, tuple) or len(pair_score) != 2:
                    #print(f"[ERROR] Invalid pair_score: {pair_score}")
                    continue

                pair, score = pair_score
                if len(pair) != 2 or not pair[0] or not pair[1]:
                    #print(f"[ERROR] Invalid pair: {pair}")
                    continue

                if pair[0] in remaining_users and pair[1] in remaining_users:
                    current_group.update(pair)

                if len(current_group) >= group_size:  
                    break

            # 残ったユーザーをすべて追加して終了
            if len(current_group) < group_size and len(remaining_users) <= group_size:
                current_group.update(remaining_users)

            # グループが作成された場合、保存する
            if len(current_group) >= 3: 
                final_groups.append({"meeting_date": meeting_date, "users": list(current_group)})
                remaining_users -= current_group
                #print(f"[DEBUG] Created group: {list(current_group)}")
            else:
                #print(f"[DEBUG] Could not form a group of size {group_size}. Remaining users: {remaining_users}")
                break
        
        if remaining_users:
            if len(remaining_users) < 3:
                # 残りの人数が3人未満の場合、組み分けしない
                print(f"[INFO] 残りのユーザーが {len(remaining_users)} 人のため、今回はグループ分けしません。: {remaining_users}")
            else:
                # 3人以上の場合、新しいグループとして作成
                final_groups.append({"meeting_date": meeting_date, "users": list(remaining_users)})
                #print(f"[DEBUG] 新しいグループを作成しました: {remaining_users}")

    return final_groups


def calculate_pair_score(participation1, participation2, user1, user2):
    """
    2人のユーザーのペアに基づきスコアを計算する。
    """
    # UserProfile を取得
    try:
        user1_profile = UserProfile.objects.get(username=user1.username)
        user2_profile = UserProfile.objects.get(username=user2.username)
    except UserProfile.DoesNotExist:
        print(f"UserProfileが見つかりません: {user1.username} または {user2.username}")
        return 0

    score = 0

    # 性別制限
    if participation1.gender_restriction == "same_gender" and user1_profile.gender == user2_profile.gender:
        score += settings.SCORING_WEIGHTS["性別制限"]["同性"]
    else:
        score += settings.SCORING_WEIGHTS["性別制限"]["希望なし"]

    # 年代制限
    age_diff = abs(user1_profile.birth_year - user2_profile.birth_year)
    if participation1.age_restriction == "same_age" and age_diff <= 2:
        score += settings.SCORING_WEIGHTS["年代制限"]["同年代"]
    elif participation1.age_restriction == "broad_age" and age_diff <= 5:
        score += settings.SCORING_WEIGHTS["年代制限"]["幅広い年代"]
    else:
        score += settings.SCORING_WEIGHTS["年代制限"]["希望なし"]

    # 入社年制限
    if participation1.joining_year_restriction == "exact_match" and user1_profile.join_year == user2_profile.join_year:
        score += settings.SCORING_WEIGHTS["入社年"]["完全一致"]
    else:
        score += settings.SCORING_WEIGHTS["入社年"]["希望なし"]

    # 部署制限
    if participation1.department_restriction == "same_department" and user1_profile.department == user2_profile.department:
        score += settings.SCORING_WEIGHTS["部署希望"]["所属部署内希望"]
    elif participation1.department_restriction == "mixed_departments":
        score += settings.SCORING_WEIGHTS["部署希望"]["他部署混在"]
    else:
        score += settings.SCORING_WEIGHTS["部署希望"]["希望なし"]

    # お店の雰囲気
    if participation1.atmosphere_preference == participation2.atmosphere_preference:
        score += settings.SCORING_WEIGHTS["お店の雰囲気"].get(participation1.atmosphere_preference, 0)
    else:
        score += settings.SCORING_WEIGHTS["お店の雰囲気"]["希望なし"]

    return score


def select_random_leader(users, excluded_leaders):
    """
    グループ内からランダムに幹事を選出。
    """

    users_as_user_objects = [User.objects.get(username=user.username) for user in users]

    potential_leaders = [user for user in users_as_user_objects if user not in excluded_leaders]

    if not potential_leaders:
        print("[INFO] 候補者がいないため除外リストをリセットします。")
        excluded_leaders.clear()
        potential_leaders = users_as_user_objects

    if not potential_leaders:
        raise ValueError("[ERROR] 候補となるユーザーが存在しません。")

    leader = random.choice(potential_leaders)
    excluded_leaders.append(leader)

    return leader


def save_groups_and_members(groups):
    """
    グループ分け結果をデータベースに保存し、メンバー情報も保存する。
    幹事も選定し、通知を送信する。
    """
    excluded_leaders = []
    saved_groups = []

    for group_data in groups:
        if not isinstance(group_data, dict):
            print(f"[ERROR] Invalid group_data type: {type(group_data)}. Skipping...")
            continue

        meeting_date = group_data["meeting_date"]
        users = UserProfile.objects.filter(username__in=[user.username for user in group_data["users"]])

        if not users:
            print(f"警告: ユーザーが存在しないグループをスキップします。日時: {meeting_date}")
            continue

        # 中間地点の座標を計算
        stations = [user.station for user in users if hasattr(user, 'station') and user.station]

        meeting_location = get_midpoint_station(stations)
        if not meeting_location:
            meeting_location = "失敗のため（仮）川崎"

        leader_profile = select_random_leader(users, excluded_leaders)

        leader_user = User.objects.get(username=leader_profile.username)

        group_obj = Group.objects.create(
            meeting_date=meeting_date,
            meeting_location=meeting_location,
            leader=leader_user
        )

        for user_profile in users:
            try:
                user = User.objects.get(username=user_profile.username)
                is_leader = (user == leader_user)

                GroupMember.objects.create(group=group_obj, user=user, is_leader=is_leader)

                Notification.objects.create(
                    user=user,
                    title="【開催決定】",
                    body=(
                        "希望日での開催が決定しました。\n"
                        "詳細は開催予定のページよりご確認ください。\n"
                        "お店については幹事より予約でき次第、追ってご連絡させて頂きます。"
                    ),
                    notification_type=NotificationType.EVENT_DECISION,
                )

                # 幹事のみに通知を送信
                if is_leader:
                    Notification.objects.create(
                        user=leader_user,
                        title="【幹事決定】",
                        body=(
                            "おめでとうございます！幹事に選出されました。\n"
                            "お店を３つ提案させていただきます。24時間以内に予約をお願いします。\n"
                            "ご予約後、予約完了報告ボタンより、予約店舗をお知らせください。"
                        ),
                        notification_type=NotificationType.MANAGER_DECISION,
                    )
            
            except User.DoesNotExist:
                print(f"[ERROR] User not found for username: {user_profile.username}")
                continue
            except Exception as e:
                print(f"[ERROR] Failed to process user {user_profile.username}: {e}")


        group_info = {
            "identifier": group_obj.identifier,
            "meeting_date": group_obj.meeting_date,
            "meeting_location": group_obj.meeting_location,
            "number_of_members": len(users),
            "users": users,
        }
        saved_groups.append(group_info)

    return saved_groups


def assign_users_to_groups():
    """
    グループ分けを実行し、幹事を選出して保存する。
    """
    groups = group_users_by_date_and_preference()
    saved_groups = save_groups_and_members(groups)

    # 幹事を抽出
    leaders = {f"Group_{idx}": group['users'][0] for idx, group in enumerate(groups) if group['users']}
    
    return saved_groups, leaders

