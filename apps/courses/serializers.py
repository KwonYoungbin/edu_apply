from rest_framework import serializers
from ..serializers import CommonSerializers
from apps.courses.models import Course

class CourseListSerializer(CommonSerializers):
    class Meta:
        model = Course
        fields = ('id', 'title', 'started_at', 'ended_at', 'created_at') 