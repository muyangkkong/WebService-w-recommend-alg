# user/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse

from .models import CustomUser
from .serializer import CreateUserSerializer  # 이미 사용 중이면 유지
# AdvertiserProfile은 advertiserList 앱으로부터 가져오기 (모델 참조는 앱명 정확히)
from advertiserList.models import AdvertiserProfile
from influencersList.models import InfluencerProfile


class SignupView(TemplateView):
    template_name = 'logg/sign_up.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({})

    def post(self, request, *args, **kwargs):
        data = {
            "username": request.POST.get("username"),
            "password": request.POST.get("password"),
            "confirm_password": request.POST.get("confirm_password"),
            "email": request.POST.get("email", "").strip(),
            "nickname": request.POST.get("nickname"),
            "field": request.POST.get("field"),
            "position": request.POST.get("user_type")
        }
        if data["password"] != data["confirm_password"]:
            messages.error(request, "Passwords do not match.")
            return render(request, self.template_name, {"data": data})

        serializer = CreateUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, "Account created. Please log in.")
            return redirect(reverse('user:login'))  # urls 네임스페이스에 맞게 조정
        return render(request, self.template_name, {"errors": serializer.errors, "data": data})


class LoginView(TemplateView):
    template_name = 'logg/login.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({})

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")
        position = request.POST.get("user_type")

        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, "Invalid credentials.")
            return render(request, self.template_name)

        if user.position != position:
            messages.error(request, "Incorrect user type.")
            return render(request, self.template_name)

        login(request, user)
        messages.success(request, "You are now logged in.")
        # 로그인 후 이동 경로: 앱 네임스페이스/URL 이름으로 지정
        if position == "influencer":
            return redirect(reverse('influencerlist:detail', kwargs={'account': user.nickname}))
        return redirect(reverse('advertiserlist:list'))


@login_required
def mypage(request):
    user = request.user
    context = {'user': user}

    if user.position == 'influencer':
        # influencer 유저에게는 마케터 목록만 제공
        context['liked_marketers'] = user.liked_marketers.all()
        context['liked_influencers'] = []  # 템플릿에서 안전하게 처리하려면 빈 리스트라도 전달
    elif user.position == 'advertiser':
        # advertiser 유저에게는 인플루언서 목록만 제공
        context['liked_influencers'] = user.liked_influencers.all()
        context['liked_marketers'] = []
    else:
        context['liked_marketers'] = []
        context['liked_influencers'] = []

    return render(request, 'logg/mypage.html', context)

def marketplace(request):
    q = request.GET.get('q', '')
    filter_role = request.GET.get('role', 'all')  # all, influencer, advertiser
    # 기본 queryset: 통합(두 모델 합치거나 모델별 탭으로 분리)
    influencers = InfluencerProfile.objects.all()
    advertisers = AdvertiserProfile.objects.all()

    return render(request, 'logg/marketplace.html', {
        'influencers': influencers,
        'advertisers': advertisers,
        'user': request.user
    })

@login_required
def like_marketer(request, marketer_id):
    marketer = get_object_or_404(AdvertiserProfile, id=marketer_id)
    request.user.liked_marketers.add(marketer)
    return redirect('user:mypage')  # 또는 원하는 URL 이름


@login_required
def unlike_marketer(request, marketer_id):
    marketer = get_object_or_404(AdvertiserProfile, id=marketer_id)
    request.user.liked_marketers.remove(marketer)
    return redirect('user:mypage')
