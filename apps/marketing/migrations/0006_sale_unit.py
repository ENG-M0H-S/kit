# Generated by Django 5.1 on 2025-04-07 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0005_remove_sale_customer_phone_remove_sale_sold_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='unit',
            field=models.CharField(blank=True, choices=[('kg', 'كيلو'), ('box', 'سلة'), ('bundle', 'ربطة'), ('cup', 'قدح'), ('bag', 'كيس')], max_length=100, null=True),
        ),
    ]
