# Generated by Django 2.1 on 2020-03-12 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notificationAndPrize', '0005_auto_20200306_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chocolate',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='discount',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
