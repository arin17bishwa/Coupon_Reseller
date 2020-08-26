from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify

# Create your models here.
HALLS=settings.HALLS


class MyAccountManager(BaseUserManager):
    def create_user(self,email,username,registration_no,password=None):
        if not email:
            raise ValueError('EMAIL ID IS REQUIRED')
        if not username:
            raise ValueError('USERNAME IS REQUIRED')
        if not password:
            raise ValueError('PASSWORD IS REQUIRED')

        user=self.model(
            email=self.normalize_email(email),
            username=username,
            registration_no=registration_no
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self,email,username,password,registration_no):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            registration_no=registration_no
        )

        user.is_admin=False
        user.is_staff = True
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self,email,username,password,registration_no):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            registration_no=registration_no,
        )

        user.is_admin=True
        user.is_staff = True
        user.is_superuser = True
        user.is_active=True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email                   = models.EmailField(verbose_name='email',max_length=60,unique=True)
    username                = models.CharField(max_length=20,unique=True)
    registration_no         = models.CharField(max_length=20,unique=True,blank=False)

    date_joined             = models.DateTimeField(verbose_name='date joined',auto_now_add=True)
    last_login              = models.DateTimeField(verbose_name='last login',auto_now=True)
    is_admin                = models.BooleanField(default=False)
    is_active               = models.BooleanField(default=False)
    is_staff                = models.BooleanField(default=False)
    is_superuser            = models.BooleanField(default=False)
    #profile                 = models.ForeignKey('UserProfile',on_delete=models.CASCADE,related_name='User_Profile')

    USERNAME_FIELD='username'
    REQUIRED_FIELDS = ['email','registration_no']
    objects=MyAccountManager()###IMPORTANT

    def __str__(self):
        return self.email

    def has_perm(self,perm,object=None):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True

class UserProfile(models.Model):
    user                =models.OneToOneField(User,on_delete=models.CASCADE)
    name                =models.CharField(max_length=50,blank=True,default='')
    hall                =models.PositiveSmallIntegerField(choices=HALLS)
    veg                 =models.BooleanField(default=False)
    slug                =models.SlugField(blank=True,unique=True)

    def __str__(self):
        return "Userame:{}\nName:{}\nHall:{}\nSlug:{}".format(self.user.username,self.name,self.hall,self.slug)

    def get_hall(self):
        return self.hall

def pre_save_userprofile(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug=slugify(instance.user.registration_no)#+'-'+datetime.datetime.now().strftime("%H%M%S%f"))

pre_save.connect(pre_save_userprofile,sender=UserProfile)