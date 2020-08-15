from django.contrib.auth import get_user_model

from rest_framework import generics, viewsets, mixins
from rest_framework.authtoken.views import ObtainAuthToken

from .models import Customer, BusinessOwner
from .serializers import CustomUserSerializer


class CustomUserCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """ 새로운 사용자를 생성한다 (회원가입) """
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer
