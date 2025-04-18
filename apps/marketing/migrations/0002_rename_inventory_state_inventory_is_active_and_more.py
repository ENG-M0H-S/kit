# Generated by Django 5.1 on 2025-03-25 23:31

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0001_initial'),
        ('plantations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='inventory',
            old_name='inventory_state',
            new_name='is_active',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='ex_date',
            new_name='expiration_date',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='product_image',
            new_name='image',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='product_state',
            new_name='is_available',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='product_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='ex_date',
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='pr_date',
        ),
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.RemoveField(
            model_name='product',
            name='pr_date',
        ),
        migrations.RemoveField(
            model_name='product',
            name='user',
        ),
        migrations.AddField(
            model_name='inventory',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='inventory',
            name='expiration_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='unit',
            field=models.CharField(choices=[('kg', 'كيلو'), ('box', 'سلة'), ('bundle', 'ربطة'), ('cup', 'قدح'), ('bag', 'كيس')], max_length=100),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='product',
            name='crop',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='plantations.crops'),
        ),
        migrations.AlterField(
            model_name='product',
            name='unit',
            field=models.CharField(choices=[('kg', 'كيلو'), ('box', 'سلة'), ('bundle', 'ربطة'), ('cup', 'قدح'), ('bag', 'كيس')], max_length=100),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('pending', 'قيد التنفيذ'), ('completed', 'مكتمل'), ('canceled', 'ملغي')], default='pending', max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderInventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('inventory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_inventories', to='marketing.inventory')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_inventories', to='marketing.order')),
            ],
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_products', to='marketing.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_products', to='marketing.product')),
            ],
        ),
        migrations.DeleteModel(
            name='Orders',
        ),
    ]
