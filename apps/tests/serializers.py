from ..serializers import CommonModelSerializer
from apps.tests.models import Test

class TestListSerializer(CommonModelSerializer):
    class Meta:
        model = Test
        fields = ('id', 'title', 'start_at', 'end_at', 'created_at')