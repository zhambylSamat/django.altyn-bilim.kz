# Generated by Django 2.1 on 2020-02-01 12:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userInfo', '0027_auto_20200118_2021'),
        ('groupsAndLessons', '0037_auto_20200201_1826'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='groupreplacement',
            unique_together={('lesson_group', 'teacher', 'date')},
        ),
    ]
