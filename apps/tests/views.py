from rest_framework import generics
from django.utils import timezone
from apps.tests.models import Test
from .serializers import TestListSerializer

class TestListAPIView(generics.ListAPIView):
    serializer_class = TestListSerializer

    def get_queryset(self):
        now = timezone.now()
        queryset = Test.objects.all()

        # 검색
        status = self.request.query_params.get('status')
        if status == 'available':  # 현재 시작 전인 시험만
            queryset = queryset.filter(started_at__gt=now)
        elif status == 'ongoing':  # 진행중인 시험
            queryset = queryset.filter(started_at__lte=now, ended_at__gte=now)
        elif status == 'finished':  # 종료된 시험
            queryset = queryset.filter(ended_at__lt=now)
            
        # 정렬
        sort = self.request.query_params.get('sort')
        if sort == 'popular': #응시자 많은 순 구현 필요
            queryset = queryset.order_by('-id')
        else:
            queryset = queryset.order_by('created_at')

        return queryset

