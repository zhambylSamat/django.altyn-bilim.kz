# Generated by Django 2.1 on 2019-12-11 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groupsAndLessons', '0012_auto_20191211_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topicplanhistory',
            name='updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
