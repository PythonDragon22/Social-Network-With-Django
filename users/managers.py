'''
from django.contrib.auth.models import BaseUserManager

# create the managers' classes here
class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        user.save()
        return user


    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True

        user.save()
        return user
'''

'''
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from users.managers import UserManager

# create the models' classes here
USER_GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
]


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=50, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)

    mobile = models.CharField(max_length=50, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    age = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=50, choices=USER_GENDER_CHOICES, null=True, blank=True)

    role = models.CharField(max_length=50, null=True, blank=True)
    bio = models.TextField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)

    user_image = models.ImageField(upload_to='user_image/', null=True, blank=True)
    cover_image = models.ImageField(upload_to='cover_image/', null=True, blank=True)
    followers = models.ManyToManyField('self', blank=True, related_name="followers")

    date_joined = models.DateTimeField(default=timezone.now)

    is_staff = models.BooleanField(default='False')
    is_superuser = models.BooleanField(default='False')
    is_active = models.BooleanField(default='True')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


    def __str__(self):
        return self.email
'''