# Generated by Django 5.1 on 2025-03-17 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(choices=[('transaction', 'معاملة'), ('season', 'موسم'), ('crop', 'محصول'), ('general', 'عامه')], max_length=50)),
                ('title', models.CharField(max_length=255)),
                ('message', models.TextField()),
            ],
        ),
        migrations.DeleteModel(
            name='Account',
        ),
    ]
