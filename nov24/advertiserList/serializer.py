from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import AdvertiserProfile

class AdvertiserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertiserProfile
        fields = '__all__'

class CreateAdvertiserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertiserProfile
        fields = '__all__'
        extra_kwargs = {
            'website': {'required': True},
            'address': {'required': True},
            'thumbnail': {'required': True},
        }