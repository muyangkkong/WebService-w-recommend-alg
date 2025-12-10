from rest_framework import serializers
from advertisement.models import Advertisement


class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = '__all__'

class CreateAdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = '__all__'
        extra_kwargs = {
            'title': {'required': True},
            'name': {'required': True},
            'description': {'required': True},
            'min_budget': {'required': True},
            'max_budget': {'required': True},
            'post_acount__nickname':{'required':True},
            'sns': {'required': True},
            'method': {'required': True},

        }
