# influencerList/models.py
from django.conf import settings
from django.db import models
from django.urls import reverse

class InfluencerProfile(models.Model):
    """
    인플루언서 프로필 모델
    - post_account: 해당 인플루언서를 소유한 User (nullable 허용)
    - display_name: 인플루언서 표시 이름 (닉네임/채널명)
    - thumbnail: 프로필 사진
    - bio / description: 소개 문구
    - method: 활동 플랫폼 (예: youtube, instagram, tiktok)
    - sns_link: 채널/프로필 URL
    - followers: 팔로워/구독자 수 (optional, 정기 업데이트용)
    - min_price/max_price: 협업 시 최소/최대 견적
    - categories: 카테고리(콤마 구분)
    """
    PLATFORM_CHOICES = (
        ('youtube', 'YouTube'),
        ('instagram', 'Instagram'),
        ('tiktok', 'TikTok'),
        ('other', 'Other'),
    )

    post_account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='influencer_profile'
    )
    display_name = models.CharField(max_length=150)
    thumbnail = models.ImageField(upload_to='influencer_thumbs/', blank=True, null=True, default='default_influencer.png')
    bio = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    method = models.CharField(max_length=30, choices=PLATFORM_CHOICES, blank=True)
    sns_link = models.URLField(max_length=400, blank=True, null=True)
    followers = models.PositiveBigIntegerField(null=True, blank=True, help_text='수동/자동으로 업데이트 가능')
    min_price = models.PositiveIntegerField(default=0)
    max_price = models.PositiveIntegerField(default=0)
    categories = models.CharField(max_length=255, blank=True, help_text='콤마로 구분된 카테고리')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Influencer Profile'
        verbose_name_plural = 'Influencer Profiles'
        indexes = [
            models.Index(fields=['display_name']),
            models.Index(fields=['method']),
        ]

    def __str__(self):
        return self.display_name or (self.post_account.nickname if self.post_account else 'Influencer')

    def get_channel_handle(self):
        """
        sns_link에서 @handle(예: youtube @handle) 또는 채널 id를 추출하는 헬퍼(템플릿/로직에서 사용)
        """
        if not self.sns_link:
            return None
        # 예: https://www.youtube.com/@handle
        import re
        m = re.search(r'youtube\.com/@([A-Za-z0-9_ -]+)', self.sns_link)
        if m:
            return m.group(1)
        # 혹은 https://www.youtube.com/channel/CHANNEL_ID
        m2 = re.search(r'youtube\.com/channel/([A-Za-z0-9_-]+)', self.sns_link)
        if m2:
            return m2.group(1)
        return None

    def get_absolute_url(self):
        return reverse('influencerlist:detail', kwargs={'pk': self.pk})
from django.db import models
