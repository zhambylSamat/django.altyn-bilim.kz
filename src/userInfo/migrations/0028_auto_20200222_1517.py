# Generated by Django 2.1 on 2020-02-22 09:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userInfo', '0027_auto_20200118_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrole',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_role', to=settings.AUTH_USER_MODEL),
        ),
    ]