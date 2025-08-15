from ..serializers import CommonSerializers
from apps.courses.models import Course

class CourseListSerializer(CommonSerializers):
    class Meta:
        model = Course
        fields = ('id', 'title', 'start_at', 'end_at', 'created_at') 