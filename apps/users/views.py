from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from apps.users.models import User
from .serializers import UserRegisterSerializer, UserLoginSerializer

class UserRegisterAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]

    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "id": user.id,
            "email": user.email
        }, status=status.HTTP_201_CREATED)
    

class UserLoginAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)