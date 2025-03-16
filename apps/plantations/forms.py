from django import forms
from apps.plantations.models import Categories, Plants


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ['category_name', 'category_image']
        

class PlantForm(forms.ModelForm):
    class Meta:
        model = Plants
        fields = ['category', 'plant_name', 'water_requirement', 'fertilizer_requirement', 
                  'harvest', 'validity', 'informations', 'image', 'img1', 'img2', 'img3']
        widgets = {
            'plant_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم النبات'}),
            'water_requirement': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'كمية الماء المطلوبة'}),
            'fertilizer_requirement': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'كمية السماد المطلوبة'}),
            'harvest': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'مدة الحصاد بالأيام'}),
            'validity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'صلاحية المنتج (اختياري)'}),
            'informations': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'معلومات إضافية'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'img1': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'img2': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'img3': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
