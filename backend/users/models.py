from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    """ 베이스 유저 모델 관리와 관련된 클래스 """

    def create_user(self, is_business_owner, email, name, birthday, phone_number, password=None):
        """ 일반 유저 생성을 위한 메소드 """
        if not email:
            raise ValueError('이메일 필드는 필수 항목입니다!')
        if not name:
            raise ValueError('이름 필드는 필수 항목입니다!')
        if not birthday:
            raise ValueError('생년월일 필드는 필수 항목입니다!')
        if not phone_number:
            raise ValueError('전화번호 필드는 필수 항목입니다!')

        email = self.normalize_email(email)
        user = self.model(is_business_owner=is_business_owner, email=email, name=name, birthday=birthday, phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, is_business_owner, email, name, birthday, phone_number, password):
        """ 슈퍼유저를 생성하는 메소드 """
        user = self.create_user(is_business_owner, email, name, birthday, phone_number, password)
        # 슈퍼유저 설정을 위한 몇가지 속성 설정
        user.is_business_owner = True
        user.is_customer = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """ 기본 베이스로 사용될 커스텀 유저 모델 """

    is_business_owner = models.BooleanField(default=False)  # 사업주 고객인 경우 True
    # is_customer = models.BooleanField()  # 일반 고객인 경우 True

    email = models.EmailField(max_length=255,
                              verbose_name='이메일 아이디',
                              unique=True,
                              help_text='아이디로 사용할 이메일 계정')
    name = models.CharField(max_length=255,
                            verbose_name='이름',
                            help_text='이름')
    birthday = models.DateField(verbose_name='생일',
                                help_text='생일')
    phone_number = models.CharField(max_length=11,
                                    verbose_name='전화번호',
                                    help_text='휴대폰 전화번호 입력(-제외)')

    # 유저 상태에 관련한 필드
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'    # 이메일을 username(ID)로 사용.
    REQUIRED_FIELDS = ['is_business_owner', 'name', 'birthday', 'phone_number']

    class Meta:
        verbose_name = '베이스 사용자'
        verbose_name_plural = '베이스 사용자'
        ordering = ('-date_joined',)

    def __str__(self):
        return self.email


class BusinessOwner(models.Model):
    """ 사업주 유저의 프로필 정보 """
    user = models.OneToOneField(CustomUser,
                                on_delete=models.CASCADE,
                                related_name='business_owner',
                                null=True)
    introduction = models.TextField(verbose_name='소개글',
                                    help_text='사업주 자신에 대한 간략한 설명')

    class Meta:
        verbose_name = '사업주'
        verbose_name_plural = '사업주'

    def __str__(self):
        return self.user.name


class Customer(models.Model):
    """ 소비자 유저의 프로필 정보 """
    user = models.OneToOneField(CustomUser,
                                on_delete=models.CASCADE,
                                related_name='customer',
                                null=True)
    nickname = models.CharField(max_length=20,
                                verbose_name='별명',
                                help_text='다른 사람들에게 보여질 이름')
    # balance = models.PositiveBigIntegerField(verbose_name='선결제 금액')

    class Meta:
        verbose_name = '소비자'
        verbose_name_plural = '소비자'

    def __str__(self):
        return self.user.name
