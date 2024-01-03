# Generated by Django 4.2.7 on 2024-01-03 14:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0003_remove_category_slug_usercategory_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='subscribers',
            field=models.ManyToManyField(related_name='categories', through='news.UserCategory', to=settings.AUTH_USER_MODEL),
        ),
    ]
