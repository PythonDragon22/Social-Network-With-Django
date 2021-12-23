from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=50, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    cover_image = models.ImageField(upload_to='cover_image/', null=True, blank=True)
    avatar = models.ImageField(upload_to='user_profile/', null=True, blank=True)
    followers = models.ManyToManyField(User, blank=True, related_name="followers")


@receiver(post_save, sender=User)
def create_user_profile(instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(instance, **kwargs):
    instance.profile.save()
