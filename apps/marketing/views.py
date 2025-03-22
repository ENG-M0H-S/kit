from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView
from apps.marketing.models import Product
from web_project import TemplateLayout



"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to sample/urls.py file for more pages.
"""


class MarketingView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        
        # جلب جميع المنتجات
        products = Product.objects.all()
        context["products"] = products


class ProductListView(ListView):
    model = Product
    template_name = "products.html"
    context_object_name = "products"
