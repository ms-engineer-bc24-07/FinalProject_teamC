from django.urls import path

from .controllers import group_controller
from .controllers.party_preference_controller import suggest_venue
from .views.home_views import HelloWorldView
from .views.participation_views import ParticipationView
from .views.user_profile_views import UserProfileView

# グループ分けされたユーザーのリストや結果を取得するエンドポイントを定義
urlpatterns = [
    path("grouped-users/", group_controller.get_grouped_users),
    path("user-profile/", UserProfileView.as_view(), name="user-profile"),
    path("participation/", ParticipationView.as_view(), name="participation"),
    path("hello/", HelloWorldView.as_view(), name="hello_world"),
]

urlpatterns = [
    path("suggest_venue/", suggest_venue, name="suggest_venue"),
]
