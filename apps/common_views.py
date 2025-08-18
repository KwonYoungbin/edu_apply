from rest_framework import generics, status
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction
from django.utils import timezone
from django.db.models import Count
from apps.payments.models import Payment
from .responses import success, error

class BaseItemListAPIView(generics.ListAPIView):
    model_field = None

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'status',
                openapi.IN_QUERY,
                description="검색 조건 (available: 신청 기간, before: 시작 전, finished: 종료)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'sort',
                openapi.IN_QUERY,
                description="정렬 조건 (created: 생성일순(default), popular: 응시자 또는 수강자 많은 순)",
                type=openapi.TYPE_STRING
            ),
        ]
    )

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if not self.model_field:
            raise NotImplementedError("model_field를 반드시 정의해야 합니다.")

        now = timezone.now()
        queryset = self.model_field.objects.all()

        status = self.request.query_params.get('status')
        if status == 'available':   # 신청 기간
            queryset = queryset.filter(start_at__lte=now, end_at__gte=now)
        elif status == 'before':    # 시작 전
            queryset = queryset.filter(start_at__gt=now)
        elif status == 'finished':  # 종료
            queryset = queryset.filter(end_at__lt=now)

        sort = self.request.query_params.get('sort')
        if sort == 'popular':
            queryset = queryset.annotate(num_registrations=Count(f'{self.model_field.__name__.lower()}registration')).order_by('-num_registrations', 'created_at')
        else:
            queryset = queryset.order_by('created_at')

        return queryset
    

class BaseApplyAPIView(APIView):
    model_field = None
    registration_field = None
    serializer_field = None
    
    @property
    def type_field(self):
        if self.model_field.__name__ == 'Test':
            return 'T'
        elif self.model_field.__name__ == 'Course':
            return 'C'
        else:
            raise ValueError('Unknown model_cls for item_type')

    def post(self, request, id):
        if not self.model_field or not self.registration_field or not self.serializer_field:
            raise NotImplementedError("모든 값을 반드시 정의해야 합니다.")

        obj = get_object_or_404(self.model_field, id=id)
        now = timezone.now()

        if now < obj.start_at or now > obj.end_at:
            return error(f'신청 가능한 기간이 아닙니다.')

        if self.registration_field.objects.filter(user=request.user, **{self.model_field.__name__.lower(): obj}).exists():
            return error(f'이미 신청한 {self.model_field.__name__}입니다.')

        serializer = self.serializer_field(data=request.data)
        if not serializer.is_valid():
            return error(errors=serializer.errors)

        amount = serializer.validated_data['amount']
        method = serializer.validated_data['payment_method']

        # 트랜잭션 처리
        with transaction.atomic():
            self.registration_field.objects.create(
                user=request.user,
                **{self.model_field.__name__.lower(): obj},
                registered_at=now
            )

            Payment.objects.create(
                user=request.user,
                item_type=self.type_field,
                item_id=obj.id,
                item_title=obj.title,
                amount=amount,
                method=method,
                paid_at=now,
            )


        return success(f'{self.model_field.__name__} 신청이 완료되었습니다.', code=status.HTTP_201_CREATED)
    
class BaseCompleteAPIView(APIView):
    model_field = None
    registration_field = None
    serializer_field = None

    def post(self, request, id):
        serializer = self.serializer_field(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            registration = self.registration_field.objects.get(user=request.user, **{f"{self.model_field.__name__.lower()}_id": id})
            if registration.completed == True:
                return error(f'이미 완료된 {self.model_field.__name__}입니다.')
            
            registration.completed = True
            registration.save()
            
            return success('처리 완료되었습니다.')

        except self.registration_field.DoesNotExist:
            return error('신청 내역이 존재하지 않습니다.', code=status.HTTP_404_NOT_FOUND)