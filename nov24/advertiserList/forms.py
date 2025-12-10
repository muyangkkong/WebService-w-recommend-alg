from django import forms
from .models import AdvertiserProfile

class AdvertiserProfileForm(forms.ModelForm):
    class Meta:
        model = AdvertiserProfile
        # 모델에 실제 있는 필드만 넣기
        fields = ('post_account', 'thumbnail', 'address', 'website', 'description')
        # 또는 전체 허용:
        # fields = '__all__'
