from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView
from apps.plantations.models import Categories, Plants, Crops
from web_project import TemplateLayout
from .forms import PlantForm, CropForm, WateringForm, FertilizationForm
from django.utils import timezone
from datetime import date, timedelta
from django.views.generic import DetailView
from django.contrib import messages
from apps.marketing.models import Product
from django.utils.timezone import now

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
    
def plants_list_view(request):
    # جلب جميع النباتات من قاعدة البيانات
    plants = Plants.objects.all()
    
    # تمرير النباتات إلى التمبلت
    return render(request, 'crop_list.html', {'plants': plants})

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

#المزروعات
class CropListView(ListView):
    model = Crops
    template_name = 'crop_list.html'
    context_object_name = 'crops'

    def get_queryset(self):
        user = self.request.user
        crop_status = self.kwargs.get('status', 'growing')  # افتراضيًا "قيد النمو"

        # جلب المحاصيل بناءً على الحالة
        if crop_status == 'growing':
            crops = Crops.objects.filter(user=user, status='growing')
        elif crop_status == 'harvested':
            crops = Crops.objects.filter(user=user, status='harvested')
        elif crop_status == 'failed':
            crops = Crops.objects.filter(user=user, status='failed')
        else:
            crops = Crops.objects.filter(user=user)

        return crops

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = self.request.user
        context['crop_list_harvested'] = Crops.objects.filter(user=user, status='harvested')
        context['crop_list_failed'] = Crops.objects.filter(user=user, status='failed')
        # إضافة معلومات إضافية
        context['page_title'] = 'قائمة المزروعات'
        context["plants"] = Plants.objects.all()
        context["layout_path"]
        return context

class CropDetailView(DetailView):
    model = Crops
    template_name = 'crop_detail.html'
    context_object_name = 'crop'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        # context = super().get_context_data(**kwargs)
        crop = self.get_object()

        # حساب عدد الأيام المتبقية لكل موعد
        def days_left(target_date):
            if target_date:
                delta = (target_date - date.today()).days
                return max(delta, 0)
            return None

        context['water_days_left'] = days_left(crop.next_watering_date)
        context['fertilizer_days_left'] = days_left(crop.next_fertilization_date)
        context['harvest_days_left'] = days_left(crop.harvest_date)
        
        context["layout_path"]
        return context
    
    
@csrf_exempt
def manage_crop(request):
    if request.method == 'POST':
        crop_id = request.POST.get('cropId', None)
        plant_id = request.POST.get('plant')
        crop_name = request.POST.get('crop_name')

        if crop_id:  # تعديل
            crop = get_object_or_404(Crops, id=crop_id)
            form = CropForm(request.POST, instance=crop)
        else:  # إضافة
            form = CropForm(request.POST)

        if form.is_valid():
            crop = form.save(commit=False)
            if not crop_id:
                crop.user = request.user  # ربط بالمستخدم الحالي فقط عند الإضافة
            crop.calculate_next_dates()  # حساب التواريخ التلقائية
            crop.save()
            return JsonResponse({
                "success": True,
                "id": crop.id,
                "message": "تم حفظ المزروع بنجاح!"
            })
        else:
            return JsonResponse({
                "success": False,
                "errors": form.errors
            })

    return JsonResponse({
        "success": False,
        "message": "طلب غير صالح"
    })
    
    
@csrf_exempt
def delete_crop(request, crop_id):
    if request.method == 'POST':
        crop = get_object_or_404(Crops, id=crop_id)
        crop.delete()
        return JsonResponse({"success": True, "message": "تم حذف المزروع بنجاح!"})
    return JsonResponse({"success": False, "error": "طلب غير صالح"}, status=400)


#الري والتسميد والتلف 
# دالة الري
def watering_crop(request, crop_id):
    crop = get_object_or_404(Crops, id=crop_id)
    crop.next_watering_date = date.today() + timedelta(days=crop.plant.water_requirement)
    crop.save()
    messages.success(request, f"تم ري المحصول '{crop.crop_name}' بنجاح.")
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({"success": True, "message": "تم ري المزروع بنجاح!"})
    return redirect('crop_detail', pk=crop.id)

# دالة التسميد
def fertilization_crop(request, crop_id):
    crop = get_object_or_404(Crops, id=crop_id)
    crop.next_fertilization_date = date.today() + timedelta(days=crop.plant.fertilizer_requirement)
    crop.save()
    messages.success(request, f"تم تسميد المحصول '{crop.crop_name}' بنجاح.")
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({"success": True, "message": "تم تسميد المزروع بنجاح!"})
    return redirect('crop_detail', pk=crop.id)


# دالة الحصاد
def harvest_crop(request, crop_id):
    crop = get_object_or_404(Crops, id=crop_id)
    plant = get_object_or_404(Plants, id=crop.plant.pk)  # جلب النبات المرتبط بالمزروع

    if crop.status == 'harvested':
        messages.warning(request, "المزروع تم حصاده بالفعل!")
        return redirect('crop_list')  # العودة إلى قائمة المحاصيل

    if request.method == 'POST':
        # جلب البيانات من النموذج
        quantity = request.POST.get('quantity')
        unit = request.POST.get('unit')
        unit_price = request.POST.get('unit_price')

        # حساب تاريخ انتهاء الصلاحية بناءً على صلاحية النبات
        expiration_date = now().date() + timedelta(days=plant.validity)

        # إنشاء المنتج في جدول المنتجات
        product = Product.objects.create(
            crop=crop,  # ربط المنتج بالمزروع
            name=plant.plant_name,  # اسم النبات
            image=plant.image,  # صورة النبات
            quantity=quantity,  # الكمية المحصودة
            unit=unit,  # الوحدة
            unit_price=unit_price,  # سعر الوحدة
            expiration_date=expiration_date,  # تاريخ انتهاء الصلاحية
            is_available=True  # تحديد المنتج كمتاح
        )

        # تحديث حالة المحصول إلى "تم حصاده"
        crop.status = 'harvested'
        if not crop.harvest_date:
            crop.harvest_date = date.today()
        crop.save()

        messages.success(request, f"تم حصاد المحصول '{crop.crop_name}' بنجاح وتم إضافة المنتج!")

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({"success": True, "message": "تم حصاد المزروع بنجاح!"})
        
        return redirect('crop_detail', pk=crop.id)  # العودة إلى تفاصيل المحصول

    return redirect('crop_detail', pk=crop.id)  # في حال لم يكن الطلب من نوع POST

# دالة التلف
def fail_crop(request, crop_id):
    crop = get_object_or_404(Crops, id=crop_id)

    # معالجة الطلب فقط إذا كان عبر POST
    if request.method == 'POST':
        crop.status = 'failed'
        crop.save()
        messages.warning(request, f"تم وضع المحصول '{crop.crop_name}' في حالة تالف.")

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({"success": True, "message": "تم اتلاف المزروع بنجاح!"})
        
        # في حالة طلب غير AJAX (مثال: من الزر العادي)
        return redirect('crop_detail', pk=crop.id)

    # في حالة إذا كان الطلب GET (لتأكيد أن المستخدم يريد التلف)
    return JsonResponse({"success": False, "message": "عملية الإتلاف لم تتم."})