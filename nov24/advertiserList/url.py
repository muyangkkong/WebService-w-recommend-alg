from django.urls import path
from . import views

urlpatterns = [
    # 템플릿
    path('', views.advertiser_list, name='advertiser_list'),
    path('create/', views.advertiser_list_post, name='advertiser_create'),

    # API
    path('api/', views.AdvertiserListAPI.as_view()),
]
# advertiserList/urls.p

