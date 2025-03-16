from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from auditlog.registry import auditlog
from django.dispatch import receiver
import random

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    account_number = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return f"Account {self.account_number} for {self.user.username}"

def generate_account_number():
    while True:
        account_number = ''.join(random.choices('0123456789', k=8))
        if not Account.objects.filter(account_number=account_number).exists():
            return account_number
        

auditlog.register(Account)
