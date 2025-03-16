from django.urls import path
from .views import MiscPagesView
from django.contrib.auth.decorators import login_required



urlpatterns = [
    path(
        "pages/misc/error/",
        login_required(MiscPagesView.as_view(template_name="pages_misc_error.html")),
        name="pages-misc-error",
    ),
    path(
        "pages/misc/under_maintenance/",
        login_required(MiscPagesView.as_view(template_name="pages_misc_under_maintenance.html")),
        name="pages-misc-under-maintenance",
    ),
    path(
        "pages/misc/comingsoon/",
        login_required(MiscPagesView.as_view(template_name="pages_misc_comingsoon.html")),
        name="pages-misc-comingsoon",
    ),
    path(
        "pages/misc/not_authorized/",
        login_required(MiscPagesView.as_view(template_name="pages_misc_not_authorized.html")),
        name="pages-misc-not-authorized",
    ),
]
