from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction
from apps.tests.models import Test
from apps.test_registrations.models import TestRegistration
from apps.payments.models import Payment
from .serializers import TestApplySerializer, TestCompleteSerializer
from ..responses import success, error

class TestApplyAPIView(APIView):
    def post(self, request, id):
        test = get_object_or_404(Test, id=id)
        now = timezone.now()

        if now >= test.start_at:
            return error('이미 시작한 시험은 신청할 수 없습니다.')

        if TestRegistration.objects.filter(user=request.user, test=test).exists():
            return error('이미 신청한 시험입니다.')

        serializer = TestApplySerializer(data=request.data)
        if not serializer.is_valid():
            return error(errors=serializer.errors)

        amount = serializer.validated_data['amount']
        method = serializer.validated_data['payment_method']

        with transaction.atomic():
            TestRegistration.objects.create(
                user=request.user,
                test=test,
                registered_at=now
            )

            Payment.objects.create(
                user=request.user,
                item_type='T',  # 'T': Test, 'C': Course
                item_id=test.id,
                item_title=test.title,
                amount=amount,
                method=method,
                status='P',     # 'P': Paid, 'C': Canceled
                paid_at=now,
                original_price=amount
            )

        return success('시험 응시가 완료되었습니다.', code=status.HTTP_201_CREATED)

class TestCompleteAPIView(APIView):
    def post(self, request, id):
        serializer = TestCompleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            registration = TestRegistration.objects.get(user=request.user, test=Test.objects.get(id=id))
            if registration.completed == True:
                return error('이미 완료한 시험입니다.')
            
            registration.completed = True
            registration.save()

            return success('시험이 완료되었습니다.')

        except TestRegistration.DoesNotExist:
            return error('신청 내역이 존재하지 않습니다.', code=status.HTTP_404_NOT_FOUND)