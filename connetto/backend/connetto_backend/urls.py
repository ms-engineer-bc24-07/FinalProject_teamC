# backend/connetto_backend/urls.py
# プロジェクト全体のURLを管理するルート設定ファイル
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path


def home_view(request):
    return HttpResponse("<h1>Welcome to Connetto Backend</h1>")


urlpatterns = [
    path("", home_view, name="home"),  # ルート URL を設定
    path("api/", include("api.urls")),  # APIルート
    path("admin/", admin.site.urls),  # 管理画面
]
