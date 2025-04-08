from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView
from .models import Product, Sale
from .forms import SaleForm
from apps.plantations.models import Categories
from web_project import TemplateLayout
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import F, Sum
from django.db import transaction
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

class ProductView(TemplateView):
    template_name = "products.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        categories = Categories.objects.all()
        categorized_products = []

        for category in categories:
            # جلب المنتجات المرتبطة بالصنف عبر crop → plant → category
            products = Product.objects.filter(
                crop__plant__category=category,
                is_available=True
            ).distinct()[:4]

            categorized_products.append({
                'category': category,
                'products': products,
            })

        context['categorized_products'] = categorized_products
        context["layout_path"]
        context["page_title"] = "المنتجات الزراعية"
        return context


class ProductByCategoryListView(ListView):
    model = Product
    template_name = 'products_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return Product.objects.filter(
            crop__plant__category__id=category_id,
            is_available=True
        ).distinct()

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        category_id = self.kwargs.get('category_id')
        current_category = Categories.objects.get(id=category_id)

        context['page_title'] = f"منتجات {current_category.category_name_ar}"
        context['current_category'] = current_category
        context['categories'] = Categories.objects.all()
        context["layout_path"]
        return context


@csrf_exempt
def direct_sell(request):
    if request.method == 'POST':
        try:
            product_id = int(request.POST.get('product_id'))
            quantity = int(request.POST.get('quantity'))

            if quantity <= 0:
                return JsonResponse({'status': 'error', 'message': 'الكمية غير صالحة.'}, status=400)

            with transaction.atomic():
                product = Product.objects.select_for_update().get(id=product_id)

                if product.quantity >= quantity:
                    total_price = product.unit_price * quantity
                    unit = product.unit  # الحصول على الوحدة

                    # إنشاء عملية البيع
                    sale = Sale.objects.create(
                        product=product,
                        quantity=quantity,
                        total_price=total_price,
                        sold_at=timezone.now(),
                        customer_name=request.user,
                        unit=unit  # تخزين الوحدة في سجل المبيعات
                    )

                    # تحديث الكمية باستخدام F() expression
                    Product.objects.filter(id=product_id).update(
                        quantity=F('quantity') - quantity
                    )

                    return JsonResponse({
                        'status': 'success',
                        'message': f"تم بيع {quantity} {unit} بسعر إجمالي {total_price} بنجاح!",
                        'new_quantity': product.quantity - quantity
                    })
                else:
                    return JsonResponse({'status': 'error', 'message': 'الكمية المطلوبة أكبر من المتوفرة.'}, status=400)

        except (Product.DoesNotExist, ValueError) as e:
            return JsonResponse({'status': 'error', 'message': 'بيانات غير صحيحة.'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'طلب غير صالح.'}, status=400)


def user_sales(request):
    user = request.user
    sales = Sale.objects.filter(product__crop__user=user).select_related('product')

    sales_data = []
    total = 0

    for sale in sales:
        sales_data.append({
            'product_name': sale.product.name,
            'quantity': sale.quantity,
            'unit': sale.unit,
            'total_price': sale.total_price,
            'sold_at': sale.sold_at.strftime('%Y-%m-%d %H:%M'),
            'customer': str(sale.customer_name),
        })
        total += sale.total_price

    return JsonResponse({
        'status': 'success',
        'sales': sales_data,
        'total_sales': total
    })

