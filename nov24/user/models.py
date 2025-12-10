# user/models.py (권장)
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    POSITION_CHOICES = (
        ('influencer', 'Influencer'),
        ('advertiser', 'Advertiser'),
    )
    FIELD_CHOICES = (
        ('fashion', 'Fashion'),
        ('food', 'Food'),
        ('health', 'Health'),
        ('other', 'Other'),
    )

    position = models.CharField(max_length=50, choices=POSITION_CHOICES, blank=True, null=True)
    nickname = models.CharField(max_length=50, unique=True)
    field = models.CharField(max_length=50, choices=FIELD_CHOICES, blank=True, null=True)

    # 좋아요 관계는 모델 선언 한 번만(related_name 고유하게)
    liked_marketers = models.ManyToManyField('advertiserList.AdvertiserProfile', blank=True, related_name='liked_by_users_marketers')
    liked_influencers = models.ManyToManyField('influencersList.InfluencerProfile', blank=True, related_name='liked_by_users_influencers')

    selected_users = models.ManyToManyField("self", blank=True, symmetrical=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'nickname']
def __str__(self):
        return self.nickname or self.username
