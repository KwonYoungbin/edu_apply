from ..serializers import CommonSerializers
from apps.tests.models import Test

class TestListSerializer(CommonSerializers):
    class Meta:
        model = Test
        fields = ('id', 'title', 'start_at', 'end_at', 'created_at')