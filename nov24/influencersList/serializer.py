from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import InfluencerProfile

class InfluencerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfluencerProfile
        fields = '__all__'

class CreateInfluencerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfluencerProfile
        fields = '__all__'
        extra_kwargs = {
            'thumbnail': {'required': True},
            'contents': {'required': True},
            'min_price': {'required': True},
            'max_price': {'required': True},
            'description': {'required': True}
        }