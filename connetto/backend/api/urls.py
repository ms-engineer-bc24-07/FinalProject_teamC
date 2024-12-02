from django.urls import path

from .controllers import group_controller

urlpatterns = [
    path("grouped-users/", group_controller.get_grouped_users),
]
