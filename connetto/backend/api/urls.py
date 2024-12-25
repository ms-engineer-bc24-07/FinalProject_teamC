# backend/api/urls.py
# api 専用のエンドポイントを管理
from django.urls import path

from .controllers import group_controller
from .controllers.party_preference_controller import suggest_venue
from .views.home_views import HelloWorldView
from .views.notification_view import (
    NotificationDetailView,
    NotificationView,
    UnreadNotificationsCountView,
)
from .views.participation_views import ParticipationView
from .views.user_profile_views import UserProfileView
from .views.venue_views import VenueView

# グループ分けされたユーザーのリストや結果を取得するエンドポイントを定義
urlpatterns = [
    path("grouped-users/", group_controller.get_grouped_users),
    path("user-profile/", UserProfileView.as_view(), name="user-profile"),
    path("participation/", ParticipationView.as_view(), name="participation"),
    path(
        "participation/<int:pk>/",
        ParticipationView.as_view(),
        name="notification-detail",
    ),
    path("notifications/", NotificationView.as_view(), name="notifications"),
    path(
        "notifications/<int:notification_id>/",
        NotificationDetailView.as_view(),
        name="notification-detail",
    ),
    path(
        "notifications/unread-count/",
        UnreadNotificationsCountView.as_view(),
        name="unread-notifications-count",
    ),
    path("hello/", HelloWorldView.as_view(), name="hello_world"),
    path("hello/", HelloWorldView.as_view(), name="hello_world"),
    path("suggest_venue/", suggest_venue, name="suggest_venue"),
    path("venues/", VenueView.as_view(), name="venue-list"),
]
