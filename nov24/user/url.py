# user/urls.py
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'user'

urlpatterns = [
    # 루트('/')로 접속하면 로그인 페이지로 리다이렉트 하게 할 경우:
    path('', views.LoginView.as_view(), name='home'),  # / -> 로그인 화면
    # 또는 루트에서 바로 마이페이지로 보내고 싶다면 auth 로그인 체크 후 redirect 처리

    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),

    path('mypage/', views.mypage, name='mypage'),

    # 좋아요 액션
    path('like/advertiser/<int:marketer_id>/', views.like_marketer, name='like_marketer'),
    path('unlike/advertiser/<int:marketer_id>/', views.unlike_marketer, name='unlike_marketer'),

    # 필요하면 추가: 프로필 edit 등
    # path('profile/edit/', views.profile_edit, name='profile_edit'),
]
