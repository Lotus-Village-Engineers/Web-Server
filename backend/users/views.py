import traceback

from django.contrib.auth import get_user_model
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from rest_framework import generics, viewsets, mixins, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from .models import Customer, BusinessOwner
from .serializers import CustomUserSerializer
from .token import account_activation_token


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


class UserActivate(APIView):
    """ 이메일 인증을 위해 전송한 URL 정보를 통해 접근하는 View """
    permission_classes = (permissions.AllowAny, )

    def get(self, request, uidb64, token):
        """ 오직 HTTP GET 방식만 처리하며, 유저를 활성화(Activation)한다. """
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))  # Base64 디코딩
            user = get_user_model().objects.get(pk=uid)      # 유저 정보를 가져온다.
        except(TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None

        try:
            # 유저가 존재하며, 이메일에 제공된 토큰과 동일한 토큰을 가지고 있는 경우
            if user is not None and account_activation_token.check_token(user, token):
                user.is_active = True   # 유저 활성화
                user.save()             # 변경 내용 DB 저장
                return Response(user.email + '계정이 활성화 되었습니다', status=status.HTTP_200_OK)
            else:
                return Response('만료된 링크입니다', status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            print(traceback.format_exc())
