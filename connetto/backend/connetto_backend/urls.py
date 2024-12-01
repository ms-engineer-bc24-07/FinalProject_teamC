# connetto_backend/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),  # 管理画面
    path('api/data-extraction/', include('data_extraction.urls')),  # データ抽出用API
    path('api/clustering/', include('clustering.urls')),  # クラスタリング用API
    path('api/scoring/', include('scoring.urls')),  # スコアリング用API
]
