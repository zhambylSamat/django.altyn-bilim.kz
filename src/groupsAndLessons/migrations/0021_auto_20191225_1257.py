# Generated by Django 2.1 on 2019-12-25 06:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groupsAndLessons', '0020_auto_20191224_1920'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='office',
            options={'ordering': ['-title']},
        ),
        migrations.AlterModelOptions(
            name='schedule',
            options={'ordering': ['week_num', 'start_time', 'finish_time']},
        ),
    ]
