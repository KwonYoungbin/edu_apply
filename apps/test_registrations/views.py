# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction
from apps.tests.models import Test
from apps.test_registrations.models import TestRegistration
from apps.payments.models import Payment
from .serializers import TestApplySerializer, TestCompleteSerializer

class TestApplyAPIView(APIView):
    def post(self, request, id):
        test = get_object_or_404(Test, id=id)
        now = timezone.now()

        # 시험 시작 전에만 응시 가능
        if now >= test.start_at:
            return Response({'detail': '이미 시작한 시험은 신청할 수 없습니다.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # 응시 이력이 있는 경우 불가능
        if TestRegistration.objects.filter(user=request.user, test=test).exists():
            return Response({'detail': '이미 신청한 시험입니다.'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = TestApplySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        amount = serializer.validated_data['amount']
        method = serializer.validated_data['payment_method']

        with transaction.atomic():
            # 시험 응시 기록 생성
            TestRegistration.objects.create(
                user=request.user,
                test=test,
                registered_at=now
            )

            # Payment 생성
            Payment.objects.create(
                user=request.user,
                item_type='T',  # 'T': Test, 'C': Course
                item_id=test.id,
                item_title=test.title,
                amount=amount,
                method=method,
                status='P',     # 'P': Paid, 'C': Canceled
                paid_at=now
            )

        return Response({'detail': '시험 응시가 완료되었습니다.'}, status=status.HTTP_201_CREATED)

class TestCompleteAPIView(APIView):
    def post(self, request, id):
        serializer = TestCompleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            registration = TestRegistration.objects.get(user=request.user, test=Test.objects.get(id=id))
            if registration.completed == True:
                return Response({'detail': '이미 완료한 시험입니다.'}, status=status.HTTP_400_BAD_REQUEST)
            
            registration.completed = True
            registration.save()
            
            return Response({'detail': '시험이 완료되었습니다.'}, status=status.HTTP_200_OK)

        except TestRegistration.DoesNotExist:
            return Response({"detail": "신청 내역이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)