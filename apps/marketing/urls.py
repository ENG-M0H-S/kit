from django.urls import path
from . import views


urlpatterns = [
   path('products/', views.ProductView.as_view(), name='products'),
   path('products/category/<int:category_id>/', views.ProductByCategoryListView.as_view(), name='products_by_category'),
   path('products/direct-sell/', views.direct_sell, name='direct_sell'),
   path('user-sales/', views.user_sales, name='user_sales'),
]
