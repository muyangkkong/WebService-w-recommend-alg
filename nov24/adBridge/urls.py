"""
URL configuration for adBridge project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # 루트('/')를 user 앱으로 연결 -> user.urls 에서 '' 패턴을 처리
    path('', include('user.url')),

    # 앱별 분리된 URL (선택)
    path('advertisement/', include('advertisement.url')),
    path('advertiserList/', include('advertiserList.url')),  # note: 파일명 .urls 맞춘다
    path('influencerList/', include('influencersList.url'))
    #path('api/', include('api_root.urls')),  # 만약 API 라우트 따로 둠
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
