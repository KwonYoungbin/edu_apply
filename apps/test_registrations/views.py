from apps.tests.models import Test
from apps.test_registrations.models import TestRegistration
from .serializers import TestApplySerializer, TestCompleteSerializer
from ..common_views import BaseApplyAPIView, BaseCompleteAPIView

class TestApplyAPIView(BaseApplyAPIView):
    model_field = Test
    registration_field = TestRegistration
    serializer_field = TestApplySerializer

class TestCompleteAPIView(BaseCompleteAPIView):
    model_field = Test
    registration_field = TestRegistration
    serializer_field = TestCompleteSerializer