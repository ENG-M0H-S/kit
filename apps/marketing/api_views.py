from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *


class ProductViewSet(viewsets.ModelViewSet):
    """
    API لإدارة المنتجات الخاصة بالمزارعين.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]  # السماح فقط للمستخدمين المسجلين بالوصول

    def perform_create(self, serializer):
        """
        عند إنشاء منتج جديد، يتم تحديد المستخدم تلقائيًا.
        """
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """
        إذا كان المستخدم مزارعًا، فسيتم عرض منتجاته فقط.
        أما المسؤول فيمكنه رؤية جميع المنتجات.
        """
        user = self.request.user
        if user.is_staff:  # مشرف يمكنه رؤية جميع المنتجات
            return Product.objects.all()
        return Product.objects.filter(user=user)  # المزارع يرى منتجاته فقط

    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        """
        دالة لتفعيل/تعطيل المنتج.
        """
        product = get_object_or_404(Product, pk=pk)
        product.product_state = not product.product_state
        product.save()
        status = "مفعل" if product.product_state else "معطل"
        return Response({"message": f"تم تغيير حالة المنتج إلى {status}."})


class InventoryViewSet(viewsets.ModelViewSet):
    """
    API لإدارة المخزون الخاص بالتجار.
    """
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAuthenticated]  # السماح فقط للمستخدمين المسجلين بالوصول

    def perform_create(self, serializer):
        """
        عند إضافة مخزون جديد، يتم تحديد المستخدم تلقائيًا.
        """
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """
        إذا كان المستخدم تاجرًا، فسيتم عرض مخزونه فقط.
        أما المسؤول فيمكنه رؤية جميع المخزونات.
        """
        user = self.request.user
        if user.is_staff:  # المشرف يمكنه رؤية جميع المخزونات
            return Inventory.objects.all()
        return Inventory.objects.filter(user=user)  # التاجر يرى مخزونه فقط

    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        """
        دالة لتفعيل/تعطيل المخزون.
        """
        inventory = get_object_or_404(Inventory, pk=pk)
        inventory.is_active = not inventory.is_active
        inventory.save()
        status = "مفعل" if inventory.is_active else "معطل"
        return Response({"message": f"تم تغيير حالة المخزون إلى {status}."})
    
    
class OrderViewSet(viewsets.ModelViewSet):
    """
    API لإدارة الطلبات.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]  # السماح فقط للمستخدمين المسجلين بالوصول

    def perform_create(self, serializer):
        """
        عند إضافة طلب جديد، يتم تحديد المستخدم تلقائيًا.
        """
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """
        إذا كان المستخدم مشرفًا، فسيتمكن من رؤية جميع الطلبات.
        أما المستخدم العادي فسيتمكن من رؤية طلباته فقط.
        """
        user = self.request.user
        if user.is_staff:  # المشرف يمكنه رؤية جميع الطلبات
            return Order.objects.all()
        return Order.objects.filter(user=user)  # المستخدم يرى طلباته فقط

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """
        دالة لتحديث حالة الطلب.
        """
        order = get_object_or_404(Order, pk=pk)
        new_status = request.data.get("status")

        if new_status not in ["pending", "confirmed", "shipped", "delivered", "canceled"]:
            return Response({"error": "حالة الطلب غير صحيحة."}, status=400)

        order.status = new_status
        order.save()
        return Response({"message": f"تم تحديث حالة الطلب إلى {order.status}."})
    
class OrderProductViewSet(viewsets.ModelViewSet):
    """
    API لإدارة المنتجات داخل الطلبات.
    """
    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductSerializer
    permission_classes = [permissions.IsAuthenticated]  # السماح فقط للمستخدمين المسجلين بالوصول

    def get_queryset(self):
        """
        المشرف يرى جميع طلبات المنتجات، والمستخدم يرى فقط المنتجات الخاصة بطلباته.
        """
        user = self.request.user
        if user.is_staff:
            return OrderProduct.objects.all()
        return OrderProduct.objects.filter(order__user=user)

    def perform_create(self, serializer):
        """
        عند إضافة منتج إلى الطلب، يجب أن يكون الطلب تابعًا للمستخدم.
        """
        order = serializer.validated_data['order']
        if order.user != self.request.user and not self.request.user.is_staff:
            return Response({"error": "لا يمكنك إضافة منتجات إلى طلب ليس لك."}, status=403)

        serializer.save()

    @action(detail=True, methods=['post'])
    def update_quantity(self, request, pk=None):
        """
        تحديث كمية المنتج داخل الطلب.
        """
        order_product = get_object_or_404(OrderProduct, pk=pk)
        new_quantity = request.data.get("quantity")

        if not new_quantity or int(new_quantity) <= 0:
            return Response({"error": "الكمية غير صحيحة."}, status=400)

        order_product.quantity = int(new_quantity)
        order_product.save()
        return Response({"message": f"تم تحديث الكمية إلى {order_product.quantity}."})

    @action(detail=True, methods=['delete'])
    def remove_product(self, request, pk=None):
        """
        إزالة منتج من الطلب.
        """
        order_product = get_object_or_404(OrderProduct, pk=pk)
        order_product.delete()
        return Response({"message": "تم حذف المنتج من الطلب بنجاح."})
    
class OrderInventoryViewSet(viewsets.ModelViewSet):
    """
    API لإدارة منتجات المخزون داخل الطلبات.
    """
    queryset = OrderInventory.objects.all()
    serializer_class = OrderInventorySerializer
    permission_classes = [permissions.IsAuthenticated]  # السماح فقط للمستخدمين المسجلين بالوصول

    def get_queryset(self):
        """
        المشرف يرى جميع الطلبات، والمستخدم يرى فقط الطلبات الخاصة به.
        """
        user = self.request.user
        if user.is_staff:
            return OrderInventory.objects.all()
        return OrderInventory.objects.filter(order__user=user)

    def perform_create(self, serializer):
        """
        عند إضافة منتج مخزون إلى الطلب، يجب أن يكون الطلب تابعًا للمستخدم.
        """
        order = serializer.validated_data['order']
        if order.user != self.request.user and not self.request.user.is_staff:
            return Response({"error": "لا يمكنك إضافة منتجات إلى طلب ليس لك."}, status=403)

        serializer.save()

    @action(detail=True, methods=['post'])
    def update_quantity(self, request, pk=None):
        """
        تحديث كمية المنتج المخزني داخل الطلب.
        """
        order_inventory = get_object_or_404(OrderInventory, pk=pk)
        new_quantity = request.data.get("quantity")

        if not new_quantity or int(new_quantity) <= 0:
            return Response({"error": "الكمية غير صحيحة."}, status=400)

        order_inventory.quantity = int(new_quantity)
        order_inventory.save()
        return Response({"message": f"تم تحديث الكمية إلى {order_inventory.quantity}."})

    @action(detail=True, methods=['delete'])
    def remove_inventory(self, request, pk=None):
        """
        إزالة منتج مخزون من الطلب.
        """
        order_inventory = get_object_or_404(OrderInventory, pk=pk)
        order_inventory.delete()
        return Response({"message": "تم حذف المنتج من الطلب بنجاح."})