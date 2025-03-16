from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Account
import random

def generate_account_number():
    while True:
        account_number = ''.join(random.choices('0123456789', k=8))
        if not Account.objects.filter(account_number=account_number).exists():
            return account_number

@receiver(post_save, sender=User)
def create_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance, account_number=generate_account_number())