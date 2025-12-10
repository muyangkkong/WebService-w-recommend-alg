# influencerList/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import influencer_list, influencer_detail_page, influencer_create_or_update, InfluencerChannelStatsAPI, InfluencerProfileViewSet

app_name = 'influencersList'

router = DefaultRouter()
router.register(r'api', InfluencerProfileViewSet, basename='influencer')  # /influencers/api/

urlpatterns = [
    path('', influencer_list, name='list'),
    path('profile/<str:account>/', influencer_detail_page, name='detail'),
    path('profile/<str:account>/edit/', influencer_create_or_update, name='edit'),
    path('api/<str:account>/stats/', InfluencerChannelStatsAPI.as_view(), name='api-stats'),
    path('', include(router.urls)),  # API router 포함 (원하면 /api/로 바꾸기)
]
