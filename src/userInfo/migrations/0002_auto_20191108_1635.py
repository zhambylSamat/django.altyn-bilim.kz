# Generated by Django 2.1 on 2019-11-08 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userInfo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='dob',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='studenthistory',
            name='dob',
            field=models.DateField(),
        ),
    ]
