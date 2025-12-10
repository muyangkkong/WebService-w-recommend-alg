# recommender.py (유틸 파일)
from collections import defaultdict, Counter
from django.utils import timezone
from datetime import timedelta

def build_user_weights(user, decay_days=30):
    """
    user: CustomUser 인스턴스
    decay_days: 오래된 좋아요는 낮춘다
    반환: {category: weight}
    """
    weights = defaultdict(float)
    now = timezone.now()

    # liked influencers + marketers 합치기
    liked_items = list(user.liked_influencers.all()) + list(user.liked_marketers.all())

    for item in liked_items:
        # item.categories 가 "fashion,food" 같은 문자열이라 가정
        cats = (item.categories or "").split(',')
        # 시간 가중치: 최근 항목일수록 1, 오래되면 작아짐 (선택사항)
        created = getattr(item, 'created_at', None)
        if created:
            age_days = max((now - created).days, 0)
            time_w = max(0.1, 1 - (age_days / decay_days))  # 1 ~ 0.1
        else:
            time_w = 1.0
        for c in cats:
            c = c.strip().lower()
            if not c:
                continue
            weights[c] += 1.0 * time_w  # 기본 가중치 1.0, 필요시 항목별 가중치 곱하기

    return dict(weights)


def score_candidates_for_user(user, candidates_qs, top_n=20):
    """
    user: CustomUser
    candidates_qs: InfluencerProfile.objects.filter(...) 같은 쿼리셋
    반환: list of (candidate, score) 내림차순
    """
    user_w = build_user_weights(user)
    if not user_w:
        # fallback: 인기순 등
        return []

    results = []
    # 간단히 in-Python으로 계산 (규모가 작을 때)
    for cand in candidates_qs:
        cats = [(x.strip().lower()) for x in (cand.categories or "").split(',') if x.strip()]
        score = 0.0
        for c in cats:
            score += user_w.get(c, 0.0)
        # 후보의 신뢰도/팔로워 보정 (예: log scale)
        followers = getattr(cand, 'followers', 0) or 0
        pop_boost = 1.0 + (min(followers, 100000) / 100000.0) * 0.3  # 최대 +30% boost
        score *= pop_boost
        results.append((cand, score))

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:top_n]
