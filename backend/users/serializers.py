from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from rest_framework import serializers

from .models import Customer, BusinessOwner
from .token import account_activation_token


class CustomUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True,
                                     min_length=8,
                                     style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True,
                                             style={'input_type': 'password'})

    class Meta:
        model = get_user_model()
        fields = (
            'id', 'email', 'password', 'password_confirm',
            'name', 'birthday', 'phone_number', 'is_business_owner'
        )
        read_only_fields = ('id', )

    def create(self, validated_data):
        """ .is_valid() 함수 호출 시 실행되는 메소드 """
        user = get_user_model().objects.create_user(
            is_business_owner=validated_data['is_business_owner'],
            email=validated_data['email'],
            name=validated_data['name'],
            birthday=validated_data['birthday'],
            phone_number=validated_data['phone_number'],
            password=validated_data['password']
        )

        user.is_active = False  # 이메일 인증을 하지 않은 경우, is_active 값을 False
        user.save()             # 변경 내용을 DB 저장

        # 이메일에 포함될 내용을 렌더링한다. ( TEMPLATE_DIR + users/account_activate_email.html )
        message = render_to_string('users/account_activate_email.html', {
            'user': user,                   # 생성된 유저 정보
            'domain': 'localhost:8000',     # 도메인 (Base URL)
            'uid': urlsafe_base64_encode(force_bytes(user.id)),  # UID 정보를 Base64 인코딩 (암호화)
            'token': account_activation_token.make_token(user)   # 토큰 발생 (생성)
        })

        mail_subject = '회원가입 인증 메일입니다.'
        to_email = user.email
        email = EmailMessage(mail_subject,  # 이메일 제목
                             message,       # 이메일 내용
                             to=['lotuskyuree@gmail.com', to_email, ]  # 이메일 수신자
                             )
        email.send()  # 이메일 전송

        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

    def validate(self, attrs):
        """ 비밀번호와 비밀번호 확인 필드값이 동일한지 검사한다. """
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError('비밀번호가 일치하지 않습니다.')
        return attrs


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ('id', 'user', 'nickname', )
        read_only_fields = ('id', 'user', )


class BusinessOwnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = BusinessOwner
        fields = ('id', 'user', 'introduction', )
        read_only_fields = ('id', 'user', )