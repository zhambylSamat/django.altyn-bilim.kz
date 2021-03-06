# Generated by Django 2.1 on 2020-02-18 13:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='postteachersalary',
            name='salary_for',
            field=models.DateField(default=datetime.date(2020, 2, 18)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='postteachersalaryhistory',
            name='salary_for',
            field=models.DateField(default=datetime.date(2020, 2, 18)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='preteachersalary',
            name='salary_for',
            field=models.DateField(default=datetime.date(2020, 2, 18)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='preteachersalaryhistory',
            name='salary_for',
            field=models.DateField(default=datetime.date(2020, 2, 18)),
            preserve_default=False,
        ),
    ]
