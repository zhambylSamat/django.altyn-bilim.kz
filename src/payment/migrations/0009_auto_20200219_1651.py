# Generated by Django 2.1 on 2020-02-19 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0008_auto_20200219_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teachercategory',
            name='teacher',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='userInfo.Staff'),
        ),
    ]