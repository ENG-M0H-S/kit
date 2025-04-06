from django.urls import path
from . import views


urlpatterns = [
   path("categories/", views.PlantationsView.as_view(template_name="categories.html"), name="categories"),  
    path("categories-view/", views.CategoriesListView.as_view(), name="categories_view"),  

    path("plants/", views.PlantationsView.as_view(template_name="plants.html"), name="plants"),
    path("plants/<int:category_id>/", views.PlantsListView.as_view(), name="plants_list"),

    path("crops/", views.CropListView.as_view(template_name="crop_list.html"), name="crops"),
    path('detail/<int:pk>/', views.CropDetailView.as_view(template_name="crop_detail.html"), name='crop_detail'),  # رابط صفحة التفاصيل
    path('crops/harvested/', views.CropListView.as_view(), {'status': 'harvested'}, name='crop_list_harvested'),  # المحاصيل التي تم حصادها
    path('crops/failed/', views.CropListView.as_view(), {'status': 'failed'}, name='crop_list_failed'),  # المحاصيل التالفة
    
    path("vegetables/", views.PlantationsView.as_view(template_name="plant_list.html"), name="vegetables"),
    path("fruits/", views.PlantationsView.as_view(template_name="plant_list.html"), name="fruits"),
    path("grains/", views.PlantationsView.as_view(template_name="plant_list.html"), name="grains"),
    path("herbs/", views.PlantationsView.as_view(template_name="plant_list.html"), name="herbs"),
    
    path("plant/<int:plant_id>/", views.PlantationsView.as_view(template_name="plant_details.html"), name="plant_details"),
    
    
    path("plants/manage/", views.manage_plant, name="manage_plant"),
    path("plants/delete/<int:plant_id>/", views.delete_plant, name="delete_plant"),
    
    
    path('crops/manage/', views.manage_crop, name='manage_crop'),
    path('crops/delete/<int:crop_id>/', views.delete_crop, name='delete_crop'),
    
    
    path('crop/<int:crop_id>/watering/', views.watering_crop, name='watering_crop'),
    path('crop/<int:crop_id>/fertilization/', views.fertilization_crop, name='fertilization_crop'),
    path('crop/<int:crop_id>/harvest/', views.harvest_crop, name='harvest_crop'),
    path('crop/<int:crop_id>/fail/', views.fail_crop, name='fail_crop'),    
]
