from django.db import models
from apps.plantations.models import Crops,Categories,Plants
from django.contrib.auth.models import User
from django.utils import timezone
from auditlog.registry import auditlog

class Product(models.Model):
    UNIT_CHOICES = [
        ('kg','كيلو'),
        ('box','سلة'),
        ('bandle','ربطة'),
        ('cup','قدح'),
        ('bag','كيس'),
    ]

    crop = models.ForeignKey(Crops, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    product_image = models.ImageField(null=True, upload_to='photo/%y/%m/%d')
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=100, choices=UNIT_CHOICES)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    pr_date = models.DateField(auto_now_add=True)
    ex_date = models.DateField()
    product_state = models.BooleanField(default=True)

    def __str__(self):
        return self.product_name
    
class Inventory(models.Model):
    UNIT_CHOICES = [
        ('kg', 'كيلو'),
        ('box', 'سلة'),
        ('bundle', 'ربطة'),
        ('cup', 'قدح'),
        ('bag', 'كيس'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plant = models.ForeignKey(Plants, on_delete=models.CASCADE)
    image = models.ImageField(null=True, upload_to='photo/%y/%m/%d')
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=150, choices=UNIT_CHOICES)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    pr_date = models.DateField(default=timezone.now)
    ex_date = models.DateField(null=True)
    inventory_state = models.BooleanField(default=True)

    def __str__(self):
        return f"Inventory of {self.type.plant_name}"
    
class Orders(models.Model):
    UNIT_CHOICES = [
        ('kg', 'كيلو'),
        ('box', 'سلة'),
        ('bundle', 'ربطة'),
        ('cup', 'قدح'),
        ('bag', 'كيس'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(Plants, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=100, choices=UNIT_CHOICES)   
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"order {self.pk} by {self.user.username}"


auditlog.register(Product)
auditlog.register(Inventory)
auditlog.register(Orders)