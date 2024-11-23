from django.contrib import admin
from django.urls import path, include
from api.views import home_view  # 追加

urlpatterns = [
    path('', home_view, name='home'),  # ルートURLを設定
    path('api/', include('api.urls')),  # APIルート
    path('admin/', admin.site.urls),   # 管理画面
]
