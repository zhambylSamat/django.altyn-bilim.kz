# Generated by Django 2.1 on 2019-11-22 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userInfo', '0007_auto_20191115_1807'),
    ]

    operations = [
        migrations.AddField(
            model_name='parent',
            name='phone',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parenthistory',
            name='phone',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
    ]
