from django.http import JsonResponse
from api.models import Group, GroupMember, Notification
from django.contrib.auth.models import User

def create_dummy_notifications(request):
    # ユーザーの取得
    user = User.objects.first()  # 適宜 ID を指定
    if not user:
        return JsonResponse({"error": "ユーザーが見つかりません！"}, status=404)

    # グループ作成
    group = Group.objects.create(
        meeting_date="2025-01-15 19:00:00", 
        meeting_location="新宿駅", 
        leader=user
    )

    # メンバー追加
    GroupMember.objects.create(group=group, user=user, is_leader=True)

    # 通知作成
    Notification.objects.create(
        user=user,
        title="【開催決定通知】グループ",
        body=f"グループの開催が決定しました！\n"
            f"日時: {group.meeting_date}\n"
            f"場所: {group.meeting_location}\n"
            f"幹事: {user.username}",
        notification_type="EVENT_DECISION",
        data={
            "meeting_date": group.meeting_date.isoformat(),
            "meeting_location": group.meeting_location,
            "members": [{"username": member.user.username} for member in group.members.all()]
        }
    )

    Notification.objects.create(
        user=user,
        title="【幹事決定通知】グループ",
        body=f"グループの幹事に選ばれました。\n"
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

    return JsonResponse({"message": "仮グループと通知を作成しました！"})
