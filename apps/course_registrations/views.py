from apps.courses.models import Course
from apps.course_registrations.models import CourseRegistration
from .serializers import CourseApplySerializer, CourseCompleteSerializer
from ..common_views import BaseApplyAPIView, BaseCompleteAPIView

class CourseApplyAPIView(BaseApplyAPIView):
    model_field = Course
    registration_field = CourseRegistration
    serializer_field = CourseApplySerializer

class CourseCompleteAPIView(BaseCompleteAPIView):
    model_field = Course
    registration_field = CourseRegistration
    serializer_field = CourseCompleteSerializer