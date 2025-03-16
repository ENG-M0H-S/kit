from django.db import models
from django.core.validators import RegexValidator
from auditlog.registry import auditlog


class Governates(models.Model):
    gv_name = models.CharField(max_length=255)

    def __str__(self):
        return self.gv_name

class Areas(models.Model):
    governates = models.ForeignKey(Governates, on_delete=models.CASCADE)
    area_name = models.CharField(max_length=255)

    def __str__(self):
        return self.area_name


class Seasons(models.Model):
    season_name = models.CharField(max_length=255)

    def __str__(self):
        return self.season_name
    
   
class AreaSeason(models.Model):
    area = models.ForeignKey(Areas, on_delete=models.CASCADE)
    season = models.ForeignKey(Seasons, on_delete=models.CASCADE)
    start_date = models.CharField(max_length=5, validators=[RegexValidator(regex=r'^\d{2}-\d{2}$')])
    end_date = models.CharField(max_length=5, validators=[RegexValidator(regex=r'^\d{2}-\d{2}$')])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['area','season'], name='unique_area_season')
        ]

    def __str__(self):
        return f"season {self.season.season_name} in {self.area.area_name}"


auditlog.register(Governates)
auditlog.register(Areas)
auditlog.register(Seasons)
auditlog.register(AreaSeason)