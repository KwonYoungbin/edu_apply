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
from apps.users.views import UserRegisterAPIView, UserLoginAPIView
from apps.tests.views import TestListAPIView
from apps.test_registrations.views import TestApplyAPIView, TestCompleteAPIView
from apps.courses.views import CourseListAPIView
from apps.course_registrations.views import CourseApplyAPIView, CourseCompleteAPIView

urlpatterns = [
    path('signup', UserRegisterAPIView.as_view(), name='user-signup'),
    path('login', UserLoginAPIView.as_view(), name='user-login'),
    path('tests', TestListAPIView.as_view(), name='test-list'),
    path('tests/<int:id>/apply', TestApplyAPIView.as_view(), name='test-apply'),
    path('tests/<int:id>/complete', TestCompleteAPIView.as_view(), name='test-complete'),
    path('courses', CourseListAPIView.as_view(), name='course-list'),
    path('courses/<int:id>/enroll', CourseApplyAPIView.as_view(), name='course-enroll'),
    path('courses/<int:id>/complete', CourseCompleteAPIView.as_view(), name='course-complete'),
]
