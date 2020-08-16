from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Customer, BusinessOwner


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    """ 유저 모델이 생성되어 DB 내부에 저장되는 경우, 조건에 맞게 프로필 모델을 생성한다. """
    print("Is Created? : ", created)

    # instance 자체가 새롭게 생성된 경우
    if created:
        # BusinessOwner 모델 생성
        if instance.is_business_owner:
            BusinessOwner.objects.create(user=instance)
        # Customer 모델 생성
        else:
            Customer.objects.create(user=instance)

