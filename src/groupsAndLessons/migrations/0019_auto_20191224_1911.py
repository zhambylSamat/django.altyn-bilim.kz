# Generated by Django 2.1 on 2019-12-24 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groupsAndLessons', '0018_auto_20191224_1909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedulehistory',
            name='changed_user_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
