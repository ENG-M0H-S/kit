from django.urls import path
from . import views


urlpatterns = [
   path("categories/", views.PlantationsView.as_view(template_name="categories.html"), name="categories"),  
    path("categories-view/", views.CategoriesListView.as_view(), name="categories_view"),  

    path("plants/", views.PlantationsView.as_view(template_name="plants.html"), name="plants"),
    path("plants/<int:category_id>/", views.PlantsListView.as_view(), name="plants_list"),

    path("vegetables/", views.PlantationsView.as_view(template_name="plant_list.html"), name="vegetables"),
    path("fruits/", views.PlantationsView.as_view(template_name="plant_list.html"), name="fruits"),
    path("grains/", views.PlantationsView.as_view(template_name="plant_list.html"), name="grains"),
    path("herbs/", views.PlantationsView.as_view(template_name="plant_list.html"), name="herbs"),
    
    path("plant/<int:plant_id>/", views.PlantationsView.as_view(template_name="plant_details.html"), name="plant_details"),
    
    
    path("plants/manage/", views.manage_plant, name="manage_plant"),
    path("plants/delete/<int:plant_id>/", views.delete_plant, name="delete_plant"),
    
]
