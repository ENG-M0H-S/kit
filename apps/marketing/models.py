from django.db import models
from apps.plantations.models import Crops, Categories, Plants
from django.contrib.auth.models import User
from django.utils import timezone
from auditlog.registry import auditlog


# الوحدات المستخدمة في البيع والشراء
UNIT_CHOICES = [
    ('kg', 'كيلو'),
    ('box', 'سلة'),
    ('bundle', 'ربطة'),
    ('cup', 'قدح'),
    ('bag', 'كيس'),
]


#جدول المنتجات (منتجات المزارعين)
class Product(models.Model):
    crop = models.OneToOneField(Crops, on_delete=models.CASCADE, related_name="product")
    name = models.CharField(max_length=255)  # نفس اسم النبات
    image = models.ImageField(null=True, upload_to='photo/%y/%m/%d')
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=100, choices=UNIT_CHOICES)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    expiration_date = models.DateField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.crop.plant.plant_name
        super().save(*args, **kwargs)
        

#جدول المخزون (منتجات التجار)    
class Inventory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="inventory")
    plant = models.ForeignKey(Plants, on_delete=models.CASCADE)
    image = models.ImageField(null=True, upload_to='photo/%y/%m/%d')
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=100, choices=UNIT_CHOICES)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    expiration_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Inventory of {self.plant.plant_name}"
    

#جدول الطلبات (Orders)    
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'قيد التنفيذ'),
        ('completed', 'مكتمل'),
        ('canceled', 'ملغي'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Order {self.pk} by {self.user.username}"
    
    
#جدول وسيط بين الطلبات والمنتجات (منتجات المزارعين)
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_products")
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=100, choices=UNIT_CHOICES, null=True, blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} {self.product.unit} of {self.product.name} in Order {self.order.pk}"
    
    
# جدول وسيط بين الطلبات والمخزون (منتجات التجار)
class OrderInventory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_inventories")
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name="order_inventories")
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=100, choices=UNIT_CHOICES, null=True, blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} {self.inventory.unit} of {self.inventory.plant.plant_name} in Order {self.order.pk}"



auditlog.register(Product)
auditlog.register(Inventory)
auditlog.register(Order)
auditlog.register(OrderProduct)
auditlog.register(OrderInventory)