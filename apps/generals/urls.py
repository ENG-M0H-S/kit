from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

# قائمة المسارات الأصلية
urlpatterns = [
    path("govarnates/", login_required(views.GeneralsView.as_view(template_name="govarnates.html")), name="govarnates"),  
    path("governates-view/", login_required(views.GovernatesListView.as_view()), name="governates_view"),  
    
    path("areas/", login_required(views.GeneralsView.as_view(template_name="areas.html")), name="areas"), 
    path("areas-view/", login_required(views.AreasListView.as_view()), name="areas_view"),  
    
    path("seasons/", login_required(views.GeneralsView.as_view(template_name="seasons.html")), name="seasons"),  
    path("seasons-view/", login_required(views.SeasonsListView.as_view()), name="seasons_view"),  
    
    path("areaseasons/", login_required(views.GeneralsView.as_view(template_name="areaseasons.html")), name="areaseasons"),  
    path("areaseasons-view/", login_required(views.AreaSeasonsListView.as_view()), name="areaseasons_view"),  
    
    path('governates/new/', login_required(views.Add_Governate), name='add_governate'),
    path('governates/edit/', login_required(views.Add_Governate), name='edit_governate'),
    path('governates/delete/<int:governate_id>/', login_required(views.Delete_Governate), name='delete_governate'),
    
    path('areas/new/', login_required(views.Add_Area), name='add_area'),
    path('areas/edit/', login_required(views.Add_Area), name='edit_area'),
    path('areas/delete/<int:area_id>/', login_required(views.Delete_Area), name='delete_area'),
    
    path('seasons/new/', login_required(views.Add_Season), name='add_season'),
    path('seasons/edit/', login_required(views.Add_Season), name='edit_season'),
    path('seasons/delete/<int:season_id>/', login_required(views.Delete_Season), name='delete_season'),
    
    path('areaseasons/new/', login_required(views.Add_Area_Season), name='add_area_season'),
    path('areaseasons/edit/', login_required(views.Add_Area_Season), name='edit_area_season'),
    path('areaseasons/delete/<int:area_season_id>/', login_required(views.Delete_Area_Season), name='delete_area_season'),
]