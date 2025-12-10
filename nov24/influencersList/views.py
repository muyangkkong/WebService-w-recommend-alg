# influencerList/views.py
import re
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# DRF imports
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView

# Google API
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# local imports - 파일/클래스 이름이 네 프로젝트와 다르면 경로 맞춰줘
from .models import InfluencerProfile
from .serializer import InfluencerProfileSerializer, CreateInfluencerProfileSerializer
#from .forms import InfluencerProfileForm  # 만약 ModelForm을 사용한다면

# initialize youtube client once (raises if API_KEY missing)
try:
    youtube = build('youtube', 'v3', developerKey=getattr(settings, 'API_KEY', None))
except Exception:
    youtube = None


# ----------------------------
# YouTube helper functions
# ----------------------------
def extract_video_id(url):
    """
    유튜브 URL에서 비디오 ID 추출 (없으면 None)
    """
    video_id_pattern = r'(?:youtube\.com\/(?:[^\/\n\s]*\/\S*\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(video_id_pattern, url or '')
    return match.group(1) if match else None


def get_channel_id_from_handle(handle):
    """
    유튜브 @handle 로부터 채널 id를 가져옴.
    handle 예: 'someHandle' (without @)
    """
    if not youtube or not handle:
        return None
    try:
        resp = youtube.channels().list(part='id', forHandle=handle).execute()
        items = resp.get('items', [])
        if items:
            return items[0].get('id')
    except HttpError:
        return None
    except Exception:
        return None
    return None


def get_channel_statistics(method, snslink, max_videos=50):
    """
    influencer 프로필의 method(예: 'youtube')와 snslink(채널 URL 또는 handle)를 받아
    요약 통계 dict 반환. 실패시 에러 정보를 포함.
    """
    try:
        if not method or method.lower() != 'youtube' or not snslink:
            return {'error': 'unsupported method or missing snslink'}

        # handle 추출 (예: https://www.youtube.com/@handle)
        handle_match = re.search(r"youtube\.com/@([a-zA-Z0-9_-]+)", snslink)
        handle = handle_match.group(1) if handle_match else None

        # 혹은 채널 id 직접 링크인 경우 (youtube.com/channel/CHANNEL_ID)
        channel_id_match = re.search(r"youtube\.com\/channel\/([a-zA-Z0-9_-]+)", snslink)
        channel_id = channel_id_match.group(1) if channel_id_match else None

        if not channel_id and handle:
            channel_id = get_channel_id_from_handle(handle)

        if not channel_id:
            return {'error': 'Channel ID not found'}

        # 채널 통계
        channel_response = youtube.channels().list(
            part='statistics',
            id=channel_id
        ).execute()

        items = channel_response.get('items', [])
        if not items:
            return {'error': 'No channel data'}

        stats = items[0].get('statistics', {})
        subscribers_count = stats.get('subscriberCount', '0')
        total_views = stats.get('viewCount', '0')

        # 채널의 최근 비디오 ID들 가져오기
        search_resp = youtube.search().list(
            channelId=channel_id,
            part='id',
            maxResults=max_videos,
            type='video',
            order='date'
        ).execute()

        video_ids = [item['id']['videoId'] for item in search_resp.get('items', []) if item.get('id', {}).get('videoId')]
        if not video_ids:
            # 채널은 있는데 비디오 없음
            return {
                'channel_id': channel_id,
                'subscribers_count': subscribers_count,
                'total_view_count': total_views,
                'videos_analyzed': 0,
            }

        # video stats
        videos_resp = youtube.videos().list(
            part='statistics',
            id=','.join(video_ids)
        ).execute()

        total_view_count = 0
        total_like_count = 0
        total_comment_count = 0
        like_rate_acc = 0.0
        count = 0

        for v in videos_resp.get('items', []):
            st = v.get('statistics', {})
            view = int(st.get('viewCount', 0))
            like = int(st.get('likeCount', 0)) if st.get('likeCount') else 0
            comment = int(st.get('commentCount', 0)) if st.get('commentCount') else 0

            total_view_count += view
            total_like_count += like
            total_comment_count += comment
            if view > 0:
                like_rate_acc += (like / view) * 100
            count += 1

        avg_views = total_view_count // count if count else 0
        avg_like_rate = round(like_rate_acc / count, 2) if count else 0.0
        avg_comments = total_comment_count // count if count else 0

        return {
            'channel_id': channel_id,
            'subscribers_count': subscribers_count,
            'total_view_count': total_view_count,
            'avg_views_per_video': avg_views,
            'avg_like_rate_percent': avg_like_rate,
            'avg_comments_per_video': avg_comments,
            'videos_analyzed': count,
        }

    except HttpError as e:
        return {'error': 'YouTube API error', 'details': str(e)}
    except Exception as e:
        return {'error': 'Server error', 'details': str(e)}


# ----------------------------
# Template views (HTML)
# ----------------------------
def influencer_list(request):
    """
    인플루언서 목록(템플릿)
    """
    profiles = InfluencerProfile.objects.all()
    return render(request, 'influencerList/list.html', {'profiles': profiles})


def influencer_detail_page(request, account):
    """
    인플루언서 마이페이지 / 상세: account는 CustomUser.nickname 같은 식별값
    """
    instance = get_object_or_404(InfluencerProfile, post_account__nickname=account)
    serializer = InfluencerProfileSerializer(instance)
    # get_channel_statistics는 API 호출이므로 실패 가능성 있음 (비동기로 바꿀 수도 있음)
    channel_stats = get_channel_statistics(serializer.data.get('method'), serializer.data.get('snslink'))
    context = {
        'profile': serializer.data,
        'channel_stats': channel_stats,
    }
    return render(request, 'influencerList/detail.html', context)


@login_required
def influencer_create_or_update(request, account):
    """
    프로필 생성/수정 폼 처리 (템플릿)
    - account: 작성자 닉네임 또는 식별자
    """
    user = request.user
    # 권한 체크: 로그인한 유저가 요청한 account와 동일한지 또는 staff인지 등
    if user.nickname != account and not user.is_staff:
        return JsonResponse({'error': '권한 없음'}, status=403)

    try:
        instance = InfluencerProfile.objects.get(post_account__nickname=account)
    except InfluencerProfile.DoesNotExist:
        instance = None

    if request.method == 'POST':
        form = InfluencerProfileForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            obj = form.save(commit=False)
            if not instance:
                obj.post_account = user
            obj.save()
            return redirect('influencerlist:detail', account=account)
    else:
        form = InfluencerProfileForm(instance=instance)

    return render(request, 'influencerList/form.html', {'form': form, 'account': account})


# ----------------------------
# API (DRF)
# ----------------------------
class InfluencerProfileViewSet(viewsets.ModelViewSet):
    """
    API: /api/influencers/  (list, create, retrieve, update, destroy)
    """
    queryset = InfluencerProfile.objects.all()
    serializer_class = InfluencerProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # 로그인한 유저를 post_account로 저장하려면:
        serializer.save(post_account=self.request.user)


# optional: 별도 endpoint로 통계만 JSON 반환
class InfluencerChannelStatsAPI(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, account, format=None):
        instance = get_object_or_404(InfluencerProfile, post_account__nickname=account)
        serializer = InfluencerProfileSerializer(instance)
        stats = get_channel_statistics(serializer.data.get('method'), serializer.data.get('snslink'))
        return Response({'profile': serializer.data, 'channel_stats': stats})
