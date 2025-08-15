from rest_framework import serializers
from ..serializers import CommonSerializer

class CourseApplySerializer(CommonSerializer):
    amount = serializers.IntegerField()
    payment_method = serializers.CharField(max_length=20)


class CourseCompleteSerializer(CommonSerializer):
    pass