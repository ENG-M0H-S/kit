
from django.contrib import admin
from django.urls import include, path
from web_project.views import SystemView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # جميع الـ API ستكون هنا
    path('api/v1/', include('config.api_urls')),  
    
    path("admin/", admin.site.urls),
    # starter urls
    path("", include("apps.usermanage.urls")),
    # pages urls
    path("", include("apps.pages.urls")),
    # auth urls
    path("", include("auth.urls")),
    # generals urls
    path("", include("apps.generals.urls")),
    # plantations urls
    path("", include("apps.plantations.urls")),
    # notifications urls
    path("", include("apps.notifications.urls")),
    # marketing urls
    path("", include("apps.marketing.urls")),
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    
handler404 = SystemView.as_view(template_name="pages_misc_error.html", status=404)
handler403 = SystemView.as_view(template_name="pages_misc_not_authorized.html", status=403)
handler400 = SystemView.as_view(template_name="pages_misc_error.html", status=400)
handler500 = SystemView.as_view(template_name="pages_misc_error.html", status=500)
