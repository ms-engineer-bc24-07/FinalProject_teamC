from django.urls import path

from .controllers import group_controller

# グループ分けされたユーザーのリストや結果を取得するエンドポイントを定義
urlpatterns = [
    path("grouped-users/", group_controller.get_grouped_users),
]
