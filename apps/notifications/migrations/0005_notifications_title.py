# Generated by Django 5.1 on 2025-03-17 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0004_seasonalert'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
