from django.urls import path

from .controllers import group_controller
from .controllers.party_preference_controller import suggest_venue

# グループ分けされたユーザーのリストや結果を取得するエンドポイントを定義
urlpatterns = [
    path("grouped-users/", group_controller.get_grouped_users),
]

urlpatterns = [
    path("suggest_venue/", suggest_venue, name="suggest_venue"),
]
