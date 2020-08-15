from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Customer, BusinessOwner


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
        user = get_user_model().objects.create_user(
            is_business_owner=validated_data['is_business_owner'],
            email=validated_data['email'],
            name=validated_data['name'],
            birthday=validated_data['birthday'],
            phone_number=validated_data['phone_number'],
            password=validated_data['password']
        )
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