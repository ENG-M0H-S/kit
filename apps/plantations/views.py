from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView
from apps.plantations.models import Categories, Plants
from web_project import TemplateLayout
from .forms import PlantForm



"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to sample/urls.py file for more pages.
"""


class PlantationsView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        
        # جلب جميع الأصناف
        categories = Categories.objects.all()
        context["categories"] = categories
         # تخزين اسم المسار الحالي في الجلسة
        category_name = None
        if self.request.path.startswith('/vegetables/'):
            category_name = "vegetable"
        elif self.request.path.startswith('/fruits/'):
            category_name = "fruite"
        elif self.request.path.startswith('/grains/'):
            category_name = "grain"
        elif self.request.path.startswith('/herbs/'):
            category_name = "herbs"
            
        if category_name:
            category = Categories.objects.filter(category_name=category_name).first()
            if category:
                context["current_category"] = category 
            
        # عرض تفاصيل نبات معين
        if 'plant_id' in self.kwargs:
            plant_id = self.kwargs['plant_id']
            context["plant"] = get_object_or_404(Plants, id=plant_id)
            context["page_title"] = "تفاصيل النبات"
            context["template_name"] = "plant_details.html"
            
            
        # تحديد الصفحة المطلوبة بناءً على المسار
        if self.request.path == '/vegetables/':
            context["plants"] = Plants.objects.filter(category__category_name="vegetable")
            context["page_title"] = "الخضروات"
        elif self.request.path == '/fruits/':
            context["plants"] = Plants.objects.filter(category__category_name="fruite")
            context["page_title"] = "الفواكه"
        elif self.request.path == '/grains/':
            context["plants"] = Plants.objects.filter(category__category_name="grain")
            context["page_title"] = "الحبوب"
        elif self.request.path == '/herbs/':
            context["plants"] = Plants.objects.filter(category__category_name="herbs")
            context["page_title"] = "الاعشاب"
        else:
            context["categories"] = Categories.objects.all()
            context["plants"] = Plants.objects.all()
        
        return context


class PlantsListView(ListView):
    model = Plants
    template_name = "plants.html"
    context_object_name = "plants"

class CategoriesListView(ListView):
    model = Categories
    template_name = "categories.html"
    context_object_name = "categories"
    
    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        category = get_object_or_404(Categories, id=category_id)
        return Plants.objects.filter(category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = get_object_or_404(Categories, id=self.kwargs.get("category_id"))
        return context
    
@csrf_exempt
def manage_plant(request):
    if request.method == 'POST':
        plant_id = request.POST.get('plantId', None)
        category_id = request.POST.get('category')
        plant_name = request.POST.get('plantName')
        water = request.POST.get('water')
        fertilizer = request.POST.get('fertilizer')
        harvest = request.POST.get('harvest')
        validity = request.POST.get('validity')
        informations = request.POST.get('informations')
        image = request.FILES.get('image')
        img1 = request.FILES.get('img1')
        img2 = request.FILES.get('img2')
        img3 = request.FILES.get('img3')

        if plant_id:  # تعديل النبات
            plant = get_object_or_404(Plants, id=plant_id)
            form = PlantForm(request.POST, request.FILES, instance=plant)
        else:  # إضافة نبات جديد
            form = PlantForm(request.POST, request.FILES)

        if form.is_valid():
            plant = form.save()
            return JsonResponse({"success": True, "id": plant.id, "message": "تم حفظ النبات بنجاح!"})
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    
    return JsonResponse({"success": False, "message": "طلب غير صالح"})

@csrf_exempt
def delete_plant(request, plant_id):
    if request.method == 'POST':
        plant = get_object_or_404(Plants, id=plant_id)
        plant.delete()
        return JsonResponse({"success": True, "message": "تم حذف النبات بنجاح!"})
    return JsonResponse({"success": False, "error": "طلب غير صالح"}, status=400)