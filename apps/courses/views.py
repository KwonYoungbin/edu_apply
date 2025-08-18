from rest_framework.views import APIView
from rest_framework import generics
from django.db.models import Count, Q
from apps.courses.models import Course, Tag
from apps.course_registrations.models import CourseRegistration
from .serializers import CourseListSerializer, RecommendedCourseSerializer
from ..common_views import BaseItemListAPIView
from ..responses import success, error

class CourseListAPIView(BaseItemListAPIView):
    serializer_class = CourseListSerializer
    model_field = Course


class RecommendedCourseAPIView(generics.ListAPIView):
    serializer_class = RecommendedCourseSerializer

    def get_queryset(self):
        user = self.request.user

        user_course_ids = CourseRegistration.objects.filter(user=user).values_list('course_id', flat=True)
        user_tag_ids = Tag.objects.filter(courses__id__in=user_course_ids).values_list('id', flat=True)

        queryset = (
            Course.objects
            .exclude(id__in=user_course_ids)
            .filter(tags__id__in=user_tag_ids)
            .annotate(similarity=Count('tags', filter=Q(tags__id__in=user_tag_ids)))
            .order_by('-similarity', 'created_at')
        )
        return queryset