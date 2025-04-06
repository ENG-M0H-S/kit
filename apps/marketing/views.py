from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView
from .models import Product
from apps.plantations.models import Categories
from web_project import TemplateLayout



"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to sample/urls.py file for more pages.
"""


class MarketingView(TemplateView):
    template_name = "marketing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Categories.objects.all()
        products_by_category = {}

        for category in categories:
            products = Product.objects.filter(crop__plant__category=category, is_available=True)[:4]
            products_by_category[category.id] = products

        context["categories"] = categories
        context["products_by_category"] = products_by_category
        return context


class ProductsByCategoryView(TemplateView):
    template_name = "products_by_category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs["category_id"]
        category = get_object_or_404(Categories, id=category_id)

        products = Product.objects.filter(crop__plant__category=category, is_available=True)
        context["category"] = category
        context["products"] = products
        return context

class CategoryProductsView(TemplateView):
    template_name = "category_products.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = self.request.user
        category_id = self.kwargs.get("category_id")
        category = get_object_or_404(Categories, id=category_id)

        products = Product.objects.filter(
            crop__plant__category=category,
            crop__user=user,
            is_available=True
        )

        context["category"] = category
        context["products"] = products
        context["page_title"] = f"منتجات {category.category_name}"
        return context
