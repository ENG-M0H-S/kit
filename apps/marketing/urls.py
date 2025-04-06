from django.urls import path
from . import views


urlpatterns = [
   
   path('products/', views.ProductsByCategoryView.as_view(template_name="products_by_category.html"), name='products_by_category'),
   path('products/category/<int:category_id>/', views.CategoryProductsView.as_view(template_name="category_products.html"), name='category_products'),
]
