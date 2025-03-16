from django.contrib import admin
from .models import AreaSeason, Governates, Areas, Seasons

admin.site.register(Governates)
admin.site.register(Areas)
admin.site.register(Seasons)
admin.site.register(AreaSeason)
