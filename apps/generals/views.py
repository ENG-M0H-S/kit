from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from web_project import TemplateLayout
from .models import AreaSeason, Governates
from apps.generals.models import Governates, Areas, Seasons
from .forms import AreaSeasonForm, GovernateForm, AreaForm, SeasonForm
import json
from django.db import IntegrityError
from django.shortcuts import render

class GeneralsView(TemplateView):
    template_name = "govarnates.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["governates"] = Governates.objects.all()  

        context["areas"] = Areas.objects.all()
        
        context["seasons"] = Seasons.objects.all()
        
        context["areaseasons"] = AreaSeason.objects.all()
        return context


    
class AreasListView(ListView):
    model = Areas
    template_name = "areas.html"
    context_object_name = "areas"
    
class SeasonsListView(ListView):
    model = Seasons
    template_name = "seasons.html"
    context_object_name = "seasons"

class AreaSeasonsListView(ListView):
    model = AreaSeason
    template_name = "areaseasons.html"
    context_object_name = "areaseasons"

class GovernatesListView(ListView):
    model = Governates
    template_name = "govarnates.html"
    context_object_name = "governates"
    
@csrf_exempt  # تعطيل CSRF مؤقتًا (يمكن تحسين ذلك بإرسال التوكن من الـ JS)
def Add_Governate(request):
    if request.method == 'POST':
        governate_id = request.POST.get('governateId', None)
        gv_name = request.POST.get('gv_name')

        if governate_id:  # إذا كانت هذه عملية تعديل
            governate = get_object_or_404(Governates, id=governate_id)
            governate.gv_name = gv_name
            governate.save()
            return JsonResponse({"success": True, "id": governate.id, "message": "تم التعديل بنجاح!"})
        else:  # إذا كانت هذه عملية إضافة
            form = GovernateForm(request.POST)
            if form.is_valid():
                new_governate = form.save()
                return JsonResponse({"success": True, "id": new_governate.id, "message": "تمت إضافة المحافظة بنجاح!"})
            else:
                return JsonResponse({"success": False, "errors": form.errors})
    else:
        return JsonResponse({"success": False, "message": "طلب غير صالح"})

    

@csrf_exempt  # تعطيل CSRF مؤقتًا (يفضل استخدام التوكن بدلًا من ذلك)
def Delete_Governate(request, governate_id):
    if request.method == 'POST':
        governate = get_object_or_404(Governates, id=governate_id)
        governate.delete()
        return JsonResponse({"success": True, "message": "تم حذف المحافظة بنجاح!"})
    
    return JsonResponse({"success": False, "error": "طلب غير صالح"}, status=400)




@csrf_exempt  # يفضل استخدام توكن CSRF بدلًا من تعطيله
def Add_Area(request):
    if request.method == 'POST':
        area_id = request.POST.get('areaId', None)
        governate_id = request.POST.get('governates')
        area_name = request.POST.get('area_name')

        if area_id:  # تعديل المنطقة
            area = get_object_or_404(Areas, id=area_id)
            area.governates_id = governate_id
            area.area_name = area_name
            area.save()
            return JsonResponse({"success": True, "id": area.id, "message": "تم تعديل المنطقة بنجاح!"})
        else:  # إضافة منطقة جديدة
            form = AreaForm(request.POST)
            if form.is_valid():
                new_area = form.save()
                return JsonResponse({"success": True, "id": new_area.id, "message": "تمت إضافة المنطقة بنجاح!"})
            else:
                return JsonResponse({"success": False, "errors": form.errors})
    
    return JsonResponse({"success": False, "message": "طلب غير صالح"})

@csrf_exempt
def Delete_Area(request, area_id):
    if request.method == 'POST':
        area = get_object_or_404(Areas, id=area_id)
        area.delete()
        return JsonResponse({"success": True, "message": "تم حذف المنطقة بنجاح!"})
    
    return JsonResponse({"success": False, "error": "طلب غير صالح"}, status=400)


@csrf_exempt
def Add_Season(request):
    if request.method == 'POST':
        season_id = request.POST.get('seasonId', None)
        season_name = request.POST.get('season_name')

        if season_id:  # عملية تعديل
            season = get_object_or_404(Seasons, id=season_id)
            season.season_name = season_name
            season.save()
            return JsonResponse({"success": True, "id": season.id, "message": "تم التعديل بنجاح!"})
        else:  # عملية إضافة
            form = SeasonForm(request.POST)
            if form.is_valid():
                new_season = form.save()
                return JsonResponse({"success": True, "id": new_season.id, "message": "تمت إضافة الموسم بنجاح!"})
            else:
                return JsonResponse({"success": False, "errors": form.errors})
    else:
        return JsonResponse({"success": False, "message": "طلب غير صالح"})

@csrf_exempt
def Delete_Season(request, season_id):
    if request.method == 'POST':
        season = get_object_or_404(Seasons, id=season_id)
        season.delete()
        return JsonResponse({"success": True, "message": "تم حذف الموسم بنجاح!"})
    
    return JsonResponse({"success": False, "error": "طلب غير صالح"}, status=400)

@csrf_exempt
def Add_Area_Season(request):
    if request.method == 'POST':
        area_season_id = request.POST.get('areaSeasonId', None)
        area_id = request.POST.get('area_id')
        season_id = request.POST.get('season_id')
        start_month = request.POST.get('start_month')
        start_day = request.POST.get('start_day')
        end_month = request.POST.get('end_month')
        end_day = request.POST.get('end_day')

        # دمج الشهر واليوم في تاريخ واحد
        start_date = f"{start_month}-{start_day}"
        end_date = f"{end_month}-{end_day}"

        # عملية التعديل
        if area_season_id:
            area_season = get_object_or_404(AreaSeason, id=area_season_id)
            area_season.area_id = area_id
            area_season.season_id = season_id
            area_season.start_date = start_date
            area_season.end_date = end_date
            try:
                area_season.save()
                return JsonResponse({"success": True, "message": "تم التعديل بنجاح!"})
            except IntegrityError:
                return JsonResponse({"success": False, "errors": {"__all__": ["هذا الموسم موجود بالفعل لهذه المنطقة."]}})
        
        # عملية الإضافة
        else:
            form_data = {
                'area': area_id,
                'season': season_id,
                'start_month': start_month,
                'start_day': start_day,
                'end_month': end_month,
                'end_day': end_day,
            }
            form = AreaSeasonForm(form_data)
            if form.is_valid():
                try:
                    new_area_season = form.save(commit=False)
                    new_area_season.start_date = start_date  # تعيين start_date يدويًا
                    new_area_season.end_date = end_date  # تعيين end_date يدويًا
                    new_area_season.save()
                    return JsonResponse({"success": True, "id": new_area_season.id, "message": "تمت إضافة موسم المنطقة بنجاح!"})
                except IntegrityError:
                    return JsonResponse({"success": False, "errors": {"__all__": ["هذا الموسم موجود بالفعل لهذه المنطقة."]}})
            else:
                return JsonResponse({"success": False, "errors": form.errors})
    else:
        return JsonResponse({"success": False, "message": "طلب غير صالح"})
    
# حذف موسم منطقة
@csrf_exempt  # تعطيل CSRF مؤقتًا
def Delete_Area_Season(request, season_id, area_season_id):
    season = get_object_or_404(Seasons, id=season_id)
    area_season = get_object_or_404(AreaSeason, id=area_season_id, season=season)
    if request.method == 'POST':
        area_season.delete()
        return JsonResponse({"success": True, "message": "تم حذف موسم المنطقة بنجاح!"})
    return JsonResponse({"success": False, "error": "طلب غير صالح"}, status=400)

def Days(request):
    days = range(1, 31)  # إنشاء قائمة بالأرقام من 1 إلى 31
    return render(request, 'areaseasons.html', {'days': days})