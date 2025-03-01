from django.urls import path

from .controllers import group_controller
from .views.user_profile_views import UserProfileView
from .views.home_views import HelloWorldView
from .views.participation_views import ParticipationView
from .views.notification_view import NotificationView
from .views.notification_view import NotificationDetailView
from .views.notification_view import UnreadNotificationsCountView
from .views.group_view import GroupListView

urlpatterns = [
    path("grouped-users/", group_controller.get_grouped_users),

    path("user-profile/", UserProfileView.as_view(), name="user-profile"),
    path('participation/', ParticipationView.as_view(), name='participation'),
    path("participation/<int:pk>/", ParticipationView.as_view(), name="notification-detail"),
    path('notifications/', NotificationView.as_view(), name='notifications'),
    path('notifications/<int:notification_id>/', NotificationDetailView.as_view(), name='notification-detail'),
    path('notifications/unread-count/', UnreadNotificationsCountView.as_view(), name='unread-notifications-count'),
    path('groups/', GroupListView.as_view(), name='group-list'),
    path('hello/', HelloWorldView.as_view(), name='hello_world'),

]
