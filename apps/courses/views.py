from apps.courses.models import Course
from .serializers import CourseListSerializer
from ..common_views import BaseItemListAPIView

class CourseListAPIView(BaseItemListAPIView):
    serializer_class = CourseListSerializer
    model_field = Course