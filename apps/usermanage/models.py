from django.db import models
from django.contrib.auth.models import User
import random
from auditlog.registry import auditlog

class Account(models.Model):
    STATUS_CHOICES = [
        ("active", "مفعل"),
        ("inactive", "معطل"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    account_number = models.CharField(max_length=16, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")

    def __str__(self):
        return f"Account {self.account_number} for {self.user.username}"

# ✅ دالة إنشاء رقم حساب فريد
def generate_account_number():
    while True:
        account_number = ''.join(random.choices('0123456789', k=16))  # 16 رقم
        if not Account.objects.filter(account_number=account_number).exists():
            return account_number


class Transactions(models.Model):
    TRANSACTION_TYPE = [
        ('deposit','ايداع'),
        ('withdraw','خصم'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=100, choices=TRANSACTION_TYPE)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.transaction_type} of {self.amount} on {self.transaction_date}"
    
    
    
auditlog.register(Account)
