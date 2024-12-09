from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse

def home_view(request):
    return HttpResponse("<h1>Welcome to Connetto Backend</h1>")

urlpatterns = [
    path("", home_view, name="home"),  # ルート URL を設定
    path("api/", include("api.urls")),  # APIルート
    path("admin/", admin.site.urls),  # 管理画面
]
