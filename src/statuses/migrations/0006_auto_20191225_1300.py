# Generated by Django 2.1 on 2019-12-25 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statuses', '0005_auto_20191225_1257'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupstatus',
            name='title',
            field=models.CharField(default=1, max_length=120),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='groupstatushistory',
            name='title',
            field=models.CharField(default=1, max_length=120),
            preserve_default=False,
        ),
    ]
