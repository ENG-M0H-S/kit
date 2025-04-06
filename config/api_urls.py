from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from apps.marketing.api_views import *
from auth.api_views import AuthViewSet


# إعداد Swagger لتوثيق API المشروع بالكامل
schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version="v1",
        description="API documentation",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="admin@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# الراوتر الرئيسي لتجميع جميع الـ API في المشروع
router = DefaultRouter()
# إضافة API من التطبيقات المختلفة

# تسجيل API auth في الراوتر الرئيسي
router.register(r'auth', AuthViewSet, basename='auth')
# تسجيل API المنتجات في الراوتر الرئيسي
router.register(r'products', ProductViewSet, basename='product')
# تسجيل API المخزون في الراوتر الرئيسي
router.register(r'inventory', InventoryViewSet, basename='inventory')
# تسجيل API الطلبات في الراوتر الرئيسي
router.register(r'orders', OrderViewSet, basename='orders')
# تسجيل API طلبات المنتجات في الراوتر الرئيسي
router.register(r'order-products', OrderProductViewSet, basename='order-products')
# تسجيل API طلبات المخزون في الراوتر الرئيسي
router.register(r'order-inventories', OrderInventoryViewSet, basename='order-inventories')

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # جميع الـ API الخاصة بالمشروع
    path('', include(router.urls)),
]
