from django.contrib import admin
from .models import AdvertiserProfile

@admin.register(AdvertiserProfile)
class AdvertiserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'post_account', 'website', 'created_at')
    search_fields = ('name', 'post_account__nickname', 'website')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')
