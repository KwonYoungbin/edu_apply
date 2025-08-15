from apps.tests.models import Test
from .serializers import TestListSerializer
from ..common_views import BaseItemListAPIView

class TestListAPIView(BaseItemListAPIView):
    serializer_class = TestListSerializer
    model_field = Test