# Generated by Django 2.1.7 on 2019-03-02 19:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tips', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tip',
            name='author',
        ),
        migrations.AddField(
            model_name='tip',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
