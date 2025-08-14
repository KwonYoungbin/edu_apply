from rest_framework import serializers
from ..serializers import CommonSerializers
from apps.tests.models import Test

class TestListSerializer(CommonSerializers):
    class Meta:
        model = Test
        fields = ('id', 'title', 'started_at', 'ended_at', 'created_at')