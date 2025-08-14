from rest_framework import serializers

class CourseApplySerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    payment_method = serializers.CharField(max_length=20)