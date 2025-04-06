from rest_framework import serializers
from .models import Product, Inventory, Order, OrderProduct, OrderInventory

# Serializer for Product Model
class ProductSerializer(serializers.ModelSerializer):
    crop_name = serializers.ReadOnlyField(source='plant.plant_name')  # جلب اسم المزروع تلقائيًا
    user = serializers.ReadOnlyField(source='crop.user.id')  # جلب المستخدم من جدول Crops
    category = serializers.ReadOnlyField(source='crop.plant.category.id')  # جلب التصنيف من النبات

    class Meta:
        model = Product
        fields = ['id', 'crop', 'crop_name', 'user', 'category', 'image', 'quantity', 'unit', 'unit_price', 'created_at','expiration_date', 'is_available']

    def create(self, validated_data):
        # احصل على النبات المرتبط بالمزروع
        crop = validated_data['crop']
        plant_image = crop.plant.image if crop.plant.image else None

        # إذا لم يقدم المستخدم صورة، يتم استخدام صورة النبات
        if not validated_data.get('image') and plant_image:
            validated_data['image'] = plant_image

        return super().create(validated_data)
    
    
# Serializer for Inventory Model
class InventorySerializer(serializers.ModelSerializer):
    plant_name = serializers.ReadOnlyField(source='plant.plant_name')  # جلب اسم النبات تلقائيًا

    class Meta:
        model = Inventory
        fields = ['id', 'user', 'plant', 'plant_name', 'image', 'quantity', 'unit', 'unit_price', 'created_at', 'expiration_date', 'is_active']

    def create(self, validated_data):
        # احصل على صورة النبات
        plant = validated_data['plant']
        plant_image = plant.image if plant.image else None

        # إذا لم يقدم المستخدم صورة، يتم استخدام صورة النبات
        if not validated_data.get('image') and plant_image:
            validated_data['image'] = plant_image

        return super().create(validated_data)
    
    
# Serializer for OrderProduct (Intermediate Table)
class OrderProductSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.crop.crop_name')  # اسم المنتج من المحصول

    class Meta:
        model = OrderProduct
        fields = ['id', 'order', 'product', 'product_name', 'quantity', 'unit', 'unit_price']

# Serializer for OrderInventory (Intermediate Table)
class OrderInventorySerializer(serializers.ModelSerializer):
    plant_name = serializers.ReadOnlyField(source='inventory.plant.plant_name')  # اسم النبات من المخزون

    class Meta:
        model = OrderInventory
        fields = ['id', 'order', 'inventory', 'plant_name', 'quantity', 'unit', 'unit_price']

# Serializer for Order Model
class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(source='orderproduct_set', many=True, read_only=True)
    inventories = OrderInventorySerializer(source='orderinventory_set', many=True, read_only=True)
    user = serializers.ReadOnlyField(source='user.id')  # جلب معرف المستخدم
    total_price = serializers.ReadOnlyField()  # يمكن حسابه تلقائيًا عند حفظ الطلب

    class Meta:
        model = Order
        fields = ['id', 'user', 'order_date', 'total_price', 'status', 'products', 'inventories']
