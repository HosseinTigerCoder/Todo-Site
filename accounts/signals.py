from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User,Profile

@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance,phone=instance.phone)

@receiver(post_save,sender=User)
def update_user_profile(sender,instance,**kwargs):
    profile = instance.profile
    if profile.phone != instance.phone:
        profile.phone = instance.phone
        profile.save()