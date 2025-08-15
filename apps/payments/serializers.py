from rest_framework import serializers
from ..serializers import CommonSerializers
from apps.payments.models import Payment
from apps.test_registrations.models import TestRegistration
from apps.course_registrations.models import CourseRegistration

class PaymentCancelSerializer(serializers.Serializer):
    pass

class PaymentListSerializer(CommonSerializers):
    item_type_display = serializers.CharField(source="get_item_type_display", read_only=True)
    registered_at = serializers.DateTimeField(source="paid_at", read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "amount",
            "method",
            "item_type",
            "item_type_display",
            "item_id",
            "item_title",
            "status",
            "registered_at"
        ]