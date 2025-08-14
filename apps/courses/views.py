from rest_framework import generics
from django.utils import timezone
from django.db.models import Count
from apps.courses.models import Course
from apps.course_registrations.models import CourseRegistration
from .serializers import CourseListSerializer

class CourseListAPIView(generics.ListAPIView):
    serializer_class = CourseListSerializer

    def get_queryset(self):
        now = timezone.now()
        queryset = Course.objects.all()

        # 검색
        status = self.request.query_params.get('status')
        if status == 'available':  # 현재 시작 전인 수업만
            queryset = queryset.filter(started_at__gt=now)
        elif status == 'ongoing':  # 진행중인 수업
            queryset = queryset.filter(started_at__lte=now, ended_at__gte=now)
        elif status == 'finished':  # 종료된 수업
            queryset = queryset.filter(ended_at__lt=now)
            
        # 정렬
        sort = self.request.query_params.get('sort')
        if sort == 'popular':
            queryset = queryset.annotate(num_registrations=Count('courseregistration')).order_by('-num_registrations')
        else:
            queryset = queryset.order_by('created_at')

        return queryset

