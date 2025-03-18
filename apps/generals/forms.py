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
    
    start_month = forms.ChoiceField(
        label="شهر البداية",
        choices=[(i, f"{i:02d}") for i in range(1, 13)],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    start_day = forms.ChoiceField(
        label="يوم البداية",
        choices=[(i, f"{i:02d}") for i in range(1, 32)],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    end_month = forms.ChoiceField(
        label="شهر النهاية",
        choices=[(i, f"{i:02d}") for i in range(1, 13)],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    end_day = forms.ChoiceField(
        label="يوم النهاية",
        choices=[(i, f"{i:02d}") for i in range(1, 32)],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = AreaSeason
        fields = ['area', 'season', 'start_month', 'start_day', 'end_month', 'end_day']

    def clean(self):
        cleaned_data = super().clean()
        start_month = cleaned_data.get('start_month')
        start_day = cleaned_data.get('start_day')
        end_month = cleaned_data.get('end_month')
        end_day = cleaned_data.get('end_day')

        # دمج الشهر واليوم في تاريخ واحد
        if start_month and start_day:
            cleaned_data['start_date'] = f"{start_month}-{start_day}"
        if end_month and end_day:
            cleaned_data['end_date'] = f"{end_month}-{end_day}"

        return cleaned_data