# Generated by Django 2.1 on 2019-12-26 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groupsAndLessons', '0026_auto_20191226_1756'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lessongroup',
            name='group_status',
        ),
        migrations.RemoveField(
            model_name='lessongrouphistory',
            name='group_status_id',
        ),
    ]