# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction
from apps.courses.models import Course
from apps.course_registrations.models import CourseRegistration
from apps.payments.models import Payment
from .serializers import CourseApplySerializer, CourseCompleteSerializer

class CourseApplyAPIView(APIView):
    def post(self, request, id):
        course = get_object_or_404(Course, id=id)
        now = timezone.now()

        # 수강신청 시작 전에만 응시 가능
        if now >= course.start_at:
            return Response({'detail': '이미 시작한 수업은 신청할 수 없습니다.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # 수강 이력이 있는 경우 불가능
        if CourseRegistration.objects.filter(user=request.user, course=course).exists():
            return Response({'detail': '이미 수강한 수업입니다.'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = CourseApplySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        amount = serializer.validated_data['amount']
        method = serializer.validated_data['payment_method']

        with transaction.atomic():
            # 수강 기록 생성
            CourseRegistration.objects.create(
                user=request.user,
                course=course,
                registered_at=now
            )

            # Payment 생성
            Payment.objects.create(
                user=request.user,
                item_type='C',  # 'T': Test, 'C': Course
                item_id=course.id,
                amount=amount,
                method=method,
                status='P',     # 'P': Paid, 'C': Canceled
                paid_at=now
            )

        return Response({'detail': '수강 신청이 완료되었습니다.'}, status=status.HTTP_201_CREATED)

class CourseCompleteAPIView(APIView):
    def post(self, request, id):
        serializer = CourseCompleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            registration = CourseRegistration.objects.get(user=request.user, course=Course.objects.get(id=id))
            if registration.completed == True:
                return Response({'detail': '이미 완료한 수업입니다.'}, status=status.HTTP_400_BAD_REQUEST)
            
            registration.completed = True
            registration.save()
            
            return Response({'detail': '수강이 완료되었습니다.'}, status=status.HTTP_200_OK)

        except CourseRegistration.DoesNotExist:
            return Response({"detail": "신청 내역이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)    