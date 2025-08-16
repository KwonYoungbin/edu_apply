from rest_framework import serializers
from ..serializers import CommonSerializer, CommonModelSerializer
from apps.payments.models import Payment

class PaymentCancelSerializer(CommonSerializer):
    pass

class PaymentListSerializer(CommonModelSerializer):
    item_type_display = serializers.CharField(source='get_item_type_display', read_only=True)
    registered_at = serializers.DateTimeField(source='paid_at', read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id',
            'amount',
            'method',
            'item_type',
            'item_type_display',
            'item_id',
            'item_title',
            'status',
            'registered_at'
        ]

class BulkPaymentItemSerializer(CommonSerializer):
    target_type = serializers.ChoiceField(choices=[('test', '시험'), ('course', '수업')])
    target_id = serializers.IntegerField()
    amount = serializers.IntegerField()

class BulkPaymentSerializer(CommonSerializer):
    payment_method = serializers.CharField(max_length=20)
    items = BulkPaymentItemSerializer(many=True)