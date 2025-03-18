import os
from celery import Celery

# تعيين إعدادات Django كإعدادات افتراضية لـ Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'starter-kit.settings')

app = Celery('starter-kit')

# تحميل الإعدادات من ملف settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# اكتشاف المهام تلقائيًا من التطبيقات المثبتة
app.autodiscover_tasks()