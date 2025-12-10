# advertiserList/models.py
from django.conf import settings
from django.db import models
from django.urls import reverse

class AdvertiserProfile(models.Model):
    """
    광고주(업체) 프로필 모델
    - post_account: (선택) 해당 광고주를 만든/소유한 유저 (CustomUser)
    - name: 광고주/회사명 (보여줄 기본 이름)
    - thumbnail: 프로필 이미지
    - description: 회사 설명
    - address / contact / website: 기본 비즈니스 정보
    - tags: 검색용 태그(단순 문자열, 필요하면 ManyToMany로 분리)
    - created_at / updated_at: 타임스탬프
    """
    post_account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='advertiser_profile'
    )
    name = models.CharField(max_length=150)
    thumbnail = models.ImageField(upload_to='advertiser_thumbs/', blank=True, null=True, default='default_advertiser.png')
    description = models.TextField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    contact_email = models.EmailField(max_length=120, blank=True, null=True)
    contact_phone = models.CharField(max_length=40, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, help_text='콤마로 구분된 태그 (예: fashion,cosmetics)')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Advertiser Profile'
        verbose_name_plural = 'Advertiser Profiles'
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name or (self.post_account.nickname if self.post_account else 'Advertiser')

    def get_absolute_url(self):
        # 템플릿 상세 페이지 경로 (앱 URL 네임에 맞춰 수정)
        return reverse('advertiserlist:detail', kwargs={'pk': self.pk})
