from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import datetime
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

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'status',
                openapi.IN_QUERY,
                description="결제 상태 (paid: 결제 완료, cancelled: 취소됨)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'from',
                openapi.IN_QUERY,
                description="조회 시작일 (YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                format="date"
            ),
            openapi.Parameter(
                'to',
                openapi.IN_QUERY,
                description="조회 종료일 (YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                format="date"
            ),
        ]
    )

    def get_queryset(self):
        queryset = Payment.objects.filter(user=self.request.user)

        status = self.request.query_params.get('status')
        if status == 'paid':
            queryset = queryset.filter(status='P')
        elif status == 'cancelled':
            queryset = queryset.filter(status='C')

        from_date = self.request.query_params.get('from')
        to_date = self.request.query_params.get('to')

        date_format = "%Y-%m-%d"

        def parse_date(date_str, field_name):
            try:
                return datetime.strptime(date_str, date_format).date()
            except (ValueError, TypeError):
                raise ValidationError({field_name: "날짜 형식은 YYYY-MM-DD 이어야 합니다."})

        if from_date:
            from_date_parsed = parse_date(from_date, "from")
            queryset = queryset.filter(paid_at__date__gte=from_date_parsed)
        if to_date:
            to_date_parsed = parse_date(to_date, "to")
            queryset = queryset.filter(paid_at__date__lte=to_date_parsed)
        

        return queryset