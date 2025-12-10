from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import InfluencerProfile


@admin.register(InfluencerProfile)
class InfluencerProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'display_name',
        'post_account',
        'method',
        'sns_link',
        'followers',
        'created_at',
    )
    search_fields = (
        'display_name',
        'post_account__nickname',
        'method',
        'sns_link',
    )
    list_filter = (
        'method',
        'created_at',
    )
    readonly_fields = (
        'created_at',
        'updated_at',
    )
