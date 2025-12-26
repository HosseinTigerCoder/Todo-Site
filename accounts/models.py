from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.core.validators import RegexValidator

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self,phone,password=None,**extra_fields):
        if not phone:
            raise ValueError('Phone number is required.')
        user = self.model(phone=phone,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,phone,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        return self.create_user(phone,password,**extra_fields)

phone_validator = RegexValidator(regex=r'^09\d{9}$',message='شماره تلفن باید با 09 آغاز شود و عدد باشد')

class User(AbstractBaseUser,PermissionsMixin):
    phone = models.CharField(max_length=11,validators=[phone_validator],unique=True)
    email = models.EmailField(unique=True,null=True)
    fullname = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["fullname"]

    objects = UserManager()

    def __str__(self):
        return self.fullname
    
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    phone = models.CharField(max_length=11,blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.fullname
    
class PasswordToken(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    token = models.CharField(max_length=200,unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.fullname