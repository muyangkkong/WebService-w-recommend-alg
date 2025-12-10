from django.urls import path
from . import views

urlpatterns = [
    path('create-advertisement/<str:account>/', views.AdvertisementAPIView.as_view()),
    path('get-all-advertisement/', views.AllAdvertisementAPIView.as_view()),
    path('my-advertisement/<str:account>/', views.AdvertisementAPIView.as_view()),
]
