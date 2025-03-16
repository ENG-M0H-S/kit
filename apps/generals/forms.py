from django import forms
from.models import AreaSeason, Governates, Areas, Seasons
from django.core.validators import RegexValidator

class GovernateForm(forms.ModelForm):
    class Meta:
        model = Governates
        fields = ['gv_name']

class AreaForm(forms.ModelForm):
    class Meta:
        model = Areas
        fields = ['governates', 'area_name']

class SeasonForm(forms.ModelForm):
    class Meta:
        model = Seasons
        fields = ['season_name']
        
class AreaSeasonForm(forms.ModelForm):
    area = forms.ModelChoiceField(
        queryset=Areas.objects.all(),
        label='المنطقة',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    season = forms.ModelChoiceField(
        queryset=Seasons.objects.all(),
        label='الموسم',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    start_date = forms.CharField(
        label="تاريخ البداية (شهر-يوم)",
        validators=[RegexValidator(regex=r'^\d{2}-\d{2}$', message="يجب أن يكون التنسيق MM-DD")],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM-DD'})
    )

    end_date = forms.CharField(
        label="تاريخ النهاية (شهر-يوم)",
        validators=[RegexValidator(regex=r'^\d{2}-\d{2}$', message="يجب أن يكون التنسيق MM-DD")],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM-DD'})
    )

    class Meta:
        model = AreaSeason
        fields = ['area', 'season', 'start_date', 'end_date']