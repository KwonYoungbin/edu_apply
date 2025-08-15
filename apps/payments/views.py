from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from django.db import transaction
from apps.payments.models import Payment
from apps.test_registrations.models import TestRegistration
from apps.course_registrations.models import CourseRegistration
from .serializers import PaymentCancelSerializer, PaymentListSerializer
from ..responses import success, error


class PaymentCancelAPIView(APIView):
    def post(self, request, id):
        serializer = PaymentCancelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        now = timezone.now()

        try:
            payment = Payment.objects.get(id=id, user=request.user)
            if payment.status == 'C':
                return error('이미 취소된 요청입니다.')
            
            if payment.item_type == 'T':
                registration = TestRegistration.objects.get(user=request.user, test_id=payment.item_id)
            else:
                registration = CourseRegistration.objects.get(user=request.user, course_id=payment.item_id)

            if registration.completed:
                return error('이미 응시 또는 수강이 완료된 결제는 취소할 수 없습니다.')

            with transaction.atomic():
                payment.status = 'C'
                payment.canceled_at = now
                payment.save()

                registration.delete()

            return success('결제가 취소되었습니다.')

        except Payment.DoesNotExist:
            return error('결제 내역이 존재하지 않습니다.', code=status.HTTP_404_NOT_FOUND)
        except (TestRegistration.DoesNotExist, CourseRegistration.DoesNotExist):
            return error('신청 내역이 존재하지 않습니다.', code=status.HTTP_404_NOT_FOUND)


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentListSerializer

    def get_queryset(self):
        queryset = Payment.objects.filter(user=self.request.user)

        status = self.request.query_params.get('status')
        if status == 'paid':
            queryset = queryset.filter(status='P')
        elif status == 'cancelled':
            queryset = queryset.filter(status='C')

        from_date = self.request.query_params.get('from')
        to_date = self.request.query_params.get('to')

        if from_date:
            queryset = queryset.filter(paid_at__date__gte=from_date)
        if to_date:
            queryset = queryset.filter(paid_at__date__lte=to_date)

        return queryset