# Generated by Django 2.1 on 2019-12-24 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groupsAndLessons', '0016_auto_20191224_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='week_num',
            field=models.IntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')]),
        ),
    ]
