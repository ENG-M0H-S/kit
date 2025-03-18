from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path(
        "notifications",
        login_required(views.NotificationsView.as_view(template_name="notifications.html")),
        name="notifications",
    ),
     path('notifications/manage/', views.manage_notification, name='manage_notification'),
    path('notifications/delete/<int:notification_id>/', views.delete_notification, name='delete_notification'),
    
]
