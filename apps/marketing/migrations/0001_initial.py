# Generated by Django 5.1 on 2025-03-22 17:34

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('plantations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='photo/%y/%m/%d')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('unit', models.CharField(choices=[('kg', 'كيلو'), ('box', 'سلة'), ('bundle', 'ربطة'), ('cup', 'قدح'), ('bag', 'كيس')], max_length=150)),
                ('unit_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('pr_date', models.DateField(default=django.utils.timezone.now)),
                ('ex_date', models.DateField(null=True)),
                ('inventory_state', models.BooleanField(default=True)),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plantations.plants')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('unit', models.CharField(choices=[('kg', 'كيلو'), ('box', 'سلة'), ('bundle', 'ربطة'), ('cup', 'قدح'), ('bag', 'كيس')], max_length=100)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.BooleanField(default=False)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plantations.plants')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=255)),
                ('product_image', models.ImageField(null=True, upload_to='photo/%y/%m/%d')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('unit', models.CharField(choices=[('kg', 'كيلو'), ('box', 'سلة'), ('bandle', 'ربطة'), ('cup', 'قدح'), ('bag', 'كيس')], max_length=100)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pr_date', models.DateField(auto_now_add=True)),
                ('ex_date', models.DateField()),
                ('product_state', models.BooleanField(default=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plantations.categories')),
                ('crop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plantations.crops')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
