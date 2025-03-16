from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from auditlog.registry import auditlog
from apps.generals.models import Areas
from apps.usermanage.models import Account, generate_account_number

class Profile(models.Model):
    USER_TYPE = [
        ('farmer','مزارع'),
        ('merchant','تاجر'),
        ('customer','عميل')    
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email = models.EmailField(max_length=100, unique=True)
    email_token = models.CharField(max_length=100, blank=True, null=True)
    forget_password_token = models.CharField(max_length=100, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    area = models.ForeignKey(Areas, on_delete=models.CASCADE, null=True, blank=True)  
    user_type = models.CharField(max_length=100, choices=USER_TYPE, null=True, blank=True)
    phone_number = models.IntegerField(unique=True, null=True, blank=True)
    image = models.ImageField(upload_to='photo/%y/%m/%d', null=True, blank=True)


    account = models.OneToOneField(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name='profile_account')    
    
    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            # Profile.objects.create(user=instance, email=instance.email)
            profile = Profile.objects.create(
            user=instance,
            email=instance.email,
            area=instance.area,
            user_type=instance.user_type,
            phone_number=instance.phone_number,
            image=instance.image
        )
        

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"



auditlog.register(Profile)
