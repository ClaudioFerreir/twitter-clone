# Generated by Django 4.1.4 on 2024-06-04 15:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('twitter', '0004_profile_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitter',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='twitter_like', to=settings.AUTH_USER_MODEL),
        ),
    ]
