# api/controllers/group_controller.py
# グループ関連ビュー
# グループ分けの結果と幹事の選出結果をAPIで返すためのコントローラ

from api.services.group_service import assign_users_to_groups
from django.http import JsonResponse


def get_grouped_users(request):
    try:
        # ユーザーを希望日時と希望条件に基づいてグループに分け、幹事を選出
        groups, group_leaders = assign_users_to_groups()

        # グループ分け結果をJSONで返す
        response_data = {
            "groups": {
                f"Group {i + 1}": [user.name for user in group]
                for i, group in enumerate(groups)
            },
            "leaders": group_leaders,
        }

        return JsonResponse(response_data, status=200)

    except Exception as e:
        # エラー発生時には適切なエラーメッセージを返す
        return JsonResponse({"error": str(e)}, status=400)
