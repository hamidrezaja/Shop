from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from .validators import validate_iranian_phone
from django.db.models.signals import post_save
from .managers import CustomUserManager
from django.dispatch import receiver
class UserType(models.IntegerChoices):
    customer= 1, _("customer")
    admin= 2, _("admin")
    superuser= 3, _("superuser")
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified=models.BooleanField(default=False)
    type=models.IntegerField(choices=UserType.choices,default=UserType.customer.value)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
class Profile (models.Model):
    user=models.OneToOneField("CustomUser",on_delete=models.CASCADE)
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    phone_num=models.CharField(max_length=12,validators=[validate_iranian_phone])
    image = models.ImageField(upload_to="profile/",default="profile/default.png")
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    
    def get_full_name(self):
        if self.first_name or self.last_name:
            return self.first_name + '  '+ self.last_name
        return 'کاربر جدید'
    
@receiver(post_save, sender=CustomUser)
def create_profile(sender,created,instance ,**kwargs):
    if created :
        Profile.objects.create(user=instance,pk=instance.pk)
    
