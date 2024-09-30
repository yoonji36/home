# backend/login/signals.py

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Profile
from django.dispatch import receiver

# 사용자가 생성될 때 자동으로 Profile도 생성되도록 함
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# 사용자 저장 시 Profile도 저장되도록 함
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
