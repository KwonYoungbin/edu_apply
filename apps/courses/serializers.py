from ..serializers import CommonModelSerializer
from apps.courses.models import Course

class CourseListSerializer(CommonModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'title', 'start_at', 'end_at', 'created_at')