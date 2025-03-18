from django.views.generic import TemplateView
from web_project import TemplateLayout
from django.views.generic import ListView
from .models import Notifications, SeasonAlert
from .forms import NotificationForm
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from celery import shared_task
from django.db.models import Q
from apps.generals.models import AreaSeason
from django.contrib.auth.models import User

class NotificationsView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        
        context["notifications"] = Notifications.objects.all()

        return context


class NotificationsListView(ListView):
    model = Notifications
    template_name = "notifications.html"
    context_object_name = "notifications"
    
@csrf_exempt
def manage_notification(request):
    if request.method == 'POST':
        notification_id = request.POST.get('notificationId', None)
        title = request.POST.get('title')
        message = request.POST.get('message')
        notification_type = request.POST.get('notification_type')

        # عملية التعديل
        if notification_id:
            notification = get_object_or_404(Notifications, id=notification_id)
            notification.title = title
            notification.message = message
            notification.notification_type = notification_type
            try:
                notification.save()
                return JsonResponse({"success": True, "message": "تم التعديل بنجاح!"})
            except Exception as e:
                return JsonResponse({"success": False, "errors": {"__all__": [str(e)]}})
        
        # عملية الإضافة
        else:
            form = NotificationForm(request.POST)
            if form.is_valid():
                try:
                    new_notification = form.save()
                    return JsonResponse({"success": True, "id": new_notification.id, "message": "تمت إضافة الإشعار بنجاح!"})
                except Exception as e:
                    return JsonResponse({"success": False, "errors": {"__all__": [str(e)]}})
            else:
                return JsonResponse({"success": False, "errors": form.errors})
    else:
        return JsonResponse({"success": False, "message": "طلب غير صالح"})
    
@csrf_exempt
def delete_notification(request, notification_id):
    if request.method == 'POST':
        notification = get_object_or_404(Notifications, id=notification_id)
        try:
            notification.delete()
            return JsonResponse({"success": True, "message": "تم حذف الإشعار بنجاح!"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    else:
        return JsonResponse({"success": False, "message": "طلب غير صالح"})
    


@shared_task
def send_season_notifications():
    now = timezone.now()  # التاريخ والوقت الحالي
    today = now.strftime("%m-%d")  # تنسيق التاريخ كـ MM-DD

    # البحث عن المواسم التي تتطابق تواريخها مع اليوم والشهر الحالي
    seasons = AreaSeason.objects.filter(
        Q(start_date=today) | Q(end_date=today)
    )

    for season in seasons:
        # تحديد نوع الإشعار بناءً على التاريخ
        if season.start_date == today:
            notification_type = "بداية"
        elif season.end_date == today:
            notification_type = "نهاية"

        # البحث عن المستخدمين في نفس المنطقة
        users = User.objects.filter(area=season.area)

        # إنشاء الإشعار
        notification = Notifications.objects.create(
            title=f"{notification_type} موسم {season.season.season_name}",
            message=f"تم الوصول إلى {notification_type} موسم {season.season.season_name} في منطقة {season.area.area_name}.",
            notification_type="season"
        )

        # إرسال الإشعارات للمستخدمين
        for user in users:
            SeasonAlert.objects.create(
                user=user,
                notification=notification,
                season=season
            )