from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import AdvertiserProfile
from .serializer import AdvertiserProfileSerializer
#json을 주고 바든ㄴ 모든 API 작업은 serializer가 담당
from .forms import AdvertiserProfileForm
#서버 검증용 도구 폼 생성기

# 템플릿 뷰
def advertiser_list(request):
    applies = AdvertiserProfile.objects.all()
    return render(request, 'advertiserList/list.html', {'applies': applies})

def advertiser_list_post(request):
    if request.method == "POST":
        form = AdvertiserProfileForm(request.POST)
        if form.is_valid():
            instance = form.save()
            return redirect('advertiser_list')
    else:
        form = AdvertiserProfileForm()
    return render(request, 'advertiserList/createList.html', {'form': form})

# APIView
class AdvertiserListAPI(APIView):
    def get(self, request):
        profiles = AdvertiserProfile.objects.all()
        serializer = AdvertiserProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AdvertiserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
