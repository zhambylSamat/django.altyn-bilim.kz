# Generated by Django 2.1 on 2019-12-30 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groupsAndLessons', '0030_auto_20191230_1816'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessongroupstudent',
            name='started_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='lessongroupstudenthistory',
            name='started_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
