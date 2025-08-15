from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from apps.users.models import User
from .serializers import UserRegisterSerializer, UserLoginSerializer
from ..responses import success

class UserRegisterAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]

    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return success('회원가입이 완료되었습니다.', {
            'id': user.id,
            'email': user.email
        }, code=status.HTTP_201_CREATED)
    

class UserLoginAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return success('로그인 되었습니다.', serializer.validated_data)