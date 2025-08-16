"""
URL configuration for EduApply project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from apps.users.views import UserRegisterAPIView, UserLoginAPIView
from apps.tests.views import TestListAPIView
from apps.test_registrations.views import TestApplyAPIView, TestCompleteAPIView
from apps.courses.views import CourseListAPIView
from apps.course_registrations.views import CourseApplyAPIView, CourseCompleteAPIView
from apps.payments.views import PaymentCancelAPIView, PaymentListAPIView, BulkPaymentAPIView

schema_view = get_schema_view(
   openapi.Info(
      title='시험 응시 및 수업 수강 신청 시스템',  # 원하는 제목 작성
      default_version='v1.0.0',  # 애플리케이션의 버전
      description='시험 응시 및 수업 수강 신청 시스템',  # 설명
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   authentication_classes=[JWTAuthentication, ]
)

urlpatterns = [
    path('signup', UserRegisterAPIView.as_view(), name='user-signup'),
    path('login', UserLoginAPIView.as_view(), name='user-login'),
    path('tests', TestListAPIView.as_view(), name='test-list'),
    path('tests/<int:id>/apply', TestApplyAPIView.as_view(), name='test-apply'),
    path('tests/<int:id>/complete', TestCompleteAPIView.as_view(), name='test-complete'),
    path('courses', CourseListAPIView.as_view(), name='course-list'),
    path('courses/<int:id>/enroll', CourseApplyAPIView.as_view(), name='course-enroll'),
    path('courses/<int:id>/complete', CourseCompleteAPIView.as_view(), name='course-complete'),
    path('me/payments', PaymentListAPIView.as_view(), name='payment-list'),
    path('payments/<int:id>/cancel', PaymentCancelAPIView.as_view(), name='payment-cancel'),
    path('bulk/payment/apply', BulkPaymentAPIView.as_view(), name='bulk-payment-apply'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
