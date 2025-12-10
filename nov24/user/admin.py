from django.contrib import admin

from user.models import CustomUser
from influencersList.models import InfluencerProfile
from advertiserList.models import AdvertiserProfile

admin.site.register(CustomUser)
#admin.site.register(InfluencerProfile)
#admin.site.register(AdvertiserProfile)
