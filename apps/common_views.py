from rest_framework import generics, status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction
from django.utils import timezone
from django.db.models import Count
from apps.payments.models import Payment
from .responses import success, error

class BaseItemListAPIView(generics.ListAPIView):
    model_field = None

    def get_queryset(self):
        if not self.model_field:
            raise NotImplementedError("model_field를 반드시 정의해야 합니다.")

        now = timezone.now()
        queryset = self.model_field.objects.all()

        status = self.request.query_params.get('status')
        if status == 'available':   # 현재 시작 전인 시험만
            queryset = queryset.filter(start_at__gt=now)
        elif status == 'ongoing':   # 진행중인 시험
            queryset = queryset.filter(start_at__lte=now, end_at__gte=now)
        elif status == 'finished':  # 종료된 시험
            queryset = queryset.filter(end_at__lt=now)

        sort = self.request.query_params.get('sort')
        if sort == 'popular':
            queryset = queryset.annotate(num_registrations=Count(f'{self.model_field.__name__.lower()}registration')).order_by('-num_registrations', 'created_at')
            # queryset = queryset.annotate(num_registrations=Count('testregistration')).order_by('-num_registrations', 'created_at')
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

        if now >= obj.start_at:
            return error(f'이미 시작한 {self.model_field.__name__}은(는) 신청할 수 없습니다.')

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
                status='P',
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