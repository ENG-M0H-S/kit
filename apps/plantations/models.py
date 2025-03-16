from django.db import models
from auditlog.registry import auditlog

class Categories(models.Model):
    TYPE_CHOICES = [
        ('fruite','الفواكه'),
        ('vegetable','الخضار'),
        ('grain','الحبوب'),
        ('herbs','الاعشاب'),
        ('ornamental','الزينة'),
    ]

    category_name = models.CharField(max_length=255, choices=TYPE_CHOICES)
    category_image = models.ImageField(upload_to='photo/%y/%m/%d')
    def __str__(self):
        return self.category_name


class Plants(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='plants', verbose_name="الصنف")
    plant_name = models.CharField(max_length=255, verbose_name="اسم النبات")
    water_requirement = models.PositiveIntegerField(verbose_name="احتياج الماء (لتر)")
    fertilizer_requirement = models.PositiveIntegerField(verbose_name="احتياج السماد (جرام)")
    harvest = models.PositiveIntegerField(verbose_name="مدة الحصاد (يوم)")
    validity = models.PositiveIntegerField(default=0, verbose_name="صلاحية المنتج (يوم)")
    informations = models.TextField(verbose_name="معلومات إضافية")

    # الحقول الخاصة بالصور
    image = models.ImageField(upload_to='plants/main/', verbose_name="الصورة الرئيسية")
    img1 = models.ImageField(upload_to='plants/extra/', blank=True, null=True, verbose_name="صورة إضافية 1")
    img2 = models.ImageField(upload_to='plants/extra/', blank=True, null=True, verbose_name="صورة إضافية 2")
    img3 = models.ImageField(upload_to='plants/extra/', blank=True, null=True, verbose_name="صورة إضافية 3")

    def __str__(self):
        return self.plant_name



auditlog.register(Categories)
auditlog.register(Plants)