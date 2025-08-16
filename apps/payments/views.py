from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import datetime
from django.utils import timezone
from django.db import transaction
from apps.payments.models import Payment
from apps.tests.models import Test
from apps.courses.models import Course
from apps.test_registrations.models import TestRegistration
from apps.course_registrations.models import CourseRegistration
from .serializers import PaymentCancelSerializer, PaymentListSerializer, BulkPaymentSerializer
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

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

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
    

class BulkPaymentAPIView(APIView):
    DISCOUNT_RULES = {
        2: 0.05,
        3: 0.10,
        4: 0.15,
        5: 0.20
    }
    MAX_DISCOUNT = 0.20

    @swagger_auto_schema(
        request_body=BulkPaymentSerializer,
        responses={201: openapi.Response("결제 완료")}
    )

    def get_object_and_validate(self, user, target_type, target_id, now):
        if target_type == 'course':
            course = Course.objects.get(id=target_id)
            if now >= course.start_at:
                raise ValueError("이미 시작한 수업은 신청할 수 없습니다.")
            if CourseRegistration.objects.filter(user=user, course=course).exists():
                raise ValueError("이미 결제한 수업입니다.")
            CourseRegistration.objects.create(user=user, course=course)
            return 'C', course.title
        elif target_type == 'test':
            test = Test.objects.get(id=target_id)
            if now >= test.start_at:
                raise ValueError("이미 시작한 시험은 신청할 수 없습니다.")
            if TestRegistration.objects.filter(user=user, test=test).exists():
                raise ValueError("이미 신청한 시험입니다.")
            TestRegistration.objects.create(user=user, test=test)
            return 'T', test.title
        else:
            raise ValueError("잘못된 target_type 입니다.")

    def post(self, request):
        serializer = BulkPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        payment_method = serializer.validated_data['payment_method']
        items = serializer.validated_data['items']

        total_amount = 0
        payment_objects = []
        now = timezone.now()

        try:
            with transaction.atomic():
                for item in items:
                    item_type, title = self.get_object_and_validate(
                        user, item['target_type'], item['target_id'], now
                    )

                    payment = Payment(
                        user=user,
                        item_type=item_type,
                        item_id=item['target_id'],
                        item_title=title,
                        amount=item['amount'],
                        method=payment_method,
                        paid_at=now,
                        original_price=item['amount'],
                    )

                    payment_objects.append(payment)
                    total_amount += payment.amount
                
                num_items = len(payment_objects)
                discount_percent = self.DISCOUNT_RULES.get(num_items, self.MAX_DISCOUNT if num_items >= 5 else 0)
                discounted_total = int(total_amount * (1 - discount_percent))

                for payment in payment_objects:
                    payment.amount = int(payment.original_price * (1 - discount_percent))
                    payment.discounted_price = payment.original_price - payment.amount
                    payment.save()

                
            return success('결제가 완료되었습니다', {"total_amount": total_amount,
                "discount_percent": discount_percent * 100,
                "final_amount": discounted_total}, status.HTTP_201_CREATED)
        except (Test.DoesNotExist, Course.DoesNotExist):
            return error('존재하지 않는 수업 또는 시험 ID가 포함되어 있습니다.', code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return error(str(e))