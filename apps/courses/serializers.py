from rest_framework import serializers
from ..serializers import CommonModelSerializer
from apps.courses.models import Course

class CourseListSerializer(CommonModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'title', 'start_at', 'end_at', 'created_at')

class RecommendedCourseSerializer(CommonModelSerializer):
    tags = serializers.SerializerMethodField()
    similarity = serializers.IntegerField(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'similarity', 'tags']
    
    def get_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]