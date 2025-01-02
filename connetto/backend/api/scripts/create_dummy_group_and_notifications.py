import os
import django
from datetime import datetime
import pytz

# Django環境をセットアップ
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "connetto_backend.settings")
django.setup()

from api.models import Group, GroupMember, Notification
from django.contrib.auth.models import User

def create_dummy_group_and_notifications():
    # データベースに既存のユーザーを取得
    leader = User.objects.get(id=3)
    if not leader:
        print("ユーザーが見つかりません！データベースを確認してください。")
        return 

    print(f"幹事ユーザーを取得: {leader.username}")

    # グループを作成
    meeting_date = datetime(2025, 1, 16, 19, 0, tzinfo=pytz.UTC)
    group = Group.objects.create(
        meeting_date=meeting_date,  # 開催日時
        meeting_location="横浜駅",  # 開催場所
        leader=leader  # 幹事
    )

    print(f"グループを作成: {group.identifier}")

    # メンバーを追加（幹事を含む）
    GroupMember.objects.create(group=group, user=leader, is_leader=True)

    print("幹事メンバーを追加")

    # 仮メンバーを追加
    dummy_users = []
    for i in range(2, 5):  # 仮に3人のメンバーを追加
        fake_user = User.objects.create(
            username=f"dummy_user_{i}",
            email=f"dummy{i}@example.com"
        )
        dummy_users.append(fake_user)
        GroupMember.objects.create(group=group, user=fake_user, is_leader=False)
        print(f"仮メンバーを追加: {fake_user.username}")

    # グループ全員に開催決定通知を送信
    members = group.members.all()
    for member in members:
        Notification.objects.create(
            user=member.user,  # 正しいユーザーを設定
            title="【開催決定通知】",
            body=f"開催が決定しました！\n"
                f"日時: {group.meeting_date}\n"
                f"場所: {group.meeting_location}\n"
                f"幹事: {leader.username}",
            notification_type="EVENT_DECISION",
            data={
                "meeting_date": group.meeting_date.isoformat(),
                "meeting_location": group.meeting_location,
                "members": [{"username": m.user.username} for m in members]
            }
        )
        print(f"開催決定通知を作成: {member.user.username}")

    # 幹事に幹事決定通知を送信
    Notification.objects.create(
        user=leader,  # 幹事に通知を送信
        title="【幹事決定通知】",
        body=f"幹事に選ばれました。お店の候補から期日までに予約をお願いします。\n"
            f"開催場所付近のお店を予約してください。",
        notification_type="MANAGER_DECISION",
        data={
            "meeting_date": group.meeting_date.isoformat(),
            "meeting_location": group.meeting_location,
            "suggested_restaurants": [
                {"name": "居酒屋A", "url": "http://example.com/restaurant-a"},
                {"name": "居酒屋B", "url": "http://example.com/restaurant-b"},
                {"name": "居酒屋C", "url": "http://example.com/restaurant-c"}
            ]
        }
    )
    print("幹事決定通知を作成")
    print("通知を送信しました！")


if __name__ == "__main__":
    create_dummy_group_and_notifications()

