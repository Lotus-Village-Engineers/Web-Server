from django.contrib.auth import get_user_model

from rest_framework import generics, viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Customer, BusinessOwner
from .serializers import CustomUserSerializer


class CustomUserCreateApiView(generics.CreateAPIView):
    """ 새로운 사용자를 생성한다 (회원가입) """
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer


class CustomUserManageApiView(generics.RetrieveUpdateAPIView):
    """ 현재 로그인되어 있는 사용자의 정보를 수정한다. """
    serializer_class = CustomUserSerializer
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        """ 로그인된 유저의 인스턴스 획득 """
        return self.request.user
