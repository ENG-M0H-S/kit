from django.db import models
from django.contrib.auth.models import User
from apps.generals.models import AreaSeason
from django.db.models.signals import post_save
from auditlog.registry import auditlog
from django.dispatch import receiver
import random

class Notifications(models.Model):
    NOTIFICATION_TYPES = [
        
        ('transaction', 'معاملة'),
        ('season', 'موسم'),
        ('crop', 'محصول'),
        ('general', 'عامه'),
    ]
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255, null= True, blank=True)
    message = models.TextField()

    def __str__(self):
        return self.title


class SeasonAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notifications, on_delete=models.CASCADE)
    season = models.ForeignKey(AreaSeason, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    def __str__(self):
        return f"Notification for season {self.season.season.season_name}"
    
    
auditlog.register(SeasonAlert)    
auditlog.register(Notifications)
