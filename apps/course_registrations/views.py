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
from ..responses import success, error

class CourseApplyAPIView(APIView):
    def post(self, request, id):
        course = get_object_or_404(Course, id=id)
        now = timezone.now()

        if now >= course.start_at:
            return error('이미 시작한 수업은 신청할 수 없습니다')

        if CourseRegistration.objects.filter(user=request.user, course=course).exists():
            return error('이미 수강한 수업입니다')

        serializer = CourseApplySerializer(data=request.data)
        if not serializer.is_valid():
            return error(errors=serializer.errors)

        amount = serializer.validated_data['amount']
        method = serializer.validated_data['payment_method']

        with transaction.atomic():
            CourseRegistration.objects.create(
                user=request.user,
                course=course,
                registered_at=now
            )

            Payment.objects.create(
                user=request.user,
                item_type='C',  # 'T': Test, 'C': Course
                item_id=course.id,
                item_title=course.title,
                amount=amount,
                method=method,
                status='P',     # 'P': Paid, 'C': Canceled
                paid_at=now
            )

        return success('수강 신청이 완료되었습니다.', code=status.HTTP_201_CREATED)

class CourseCompleteAPIView(APIView):
    def post(self, request, id):
        serializer = CourseCompleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            registration = CourseRegistration.objects.get(user=request.user, course=Course.objects.get(id=id))
            if registration.completed == True:
                return error('이미 완료한 수업입니다.')
            
            registration.completed = True
            registration.save()
            
            return success('수강이 완료되었습니다.')

        except CourseRegistration.DoesNotExist:
            return error('신청 내역이 존재하지 않습니다.', code=status.HTTP_404_NOT_FOUND)