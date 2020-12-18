# Generated by Django 2.1 on 2020-03-12 13:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessonProgress', '0028_auto_20200310_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupstudentvisit',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='groupstudentvisithistory',
            name='updated_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='lessontestaction',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='lessontestactionhistory',
            name='updated_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='lessonvideoaction',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='lessonvideoactionhistory',
            name='updated_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='studentvisithistory',
            name='updated_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='topicquizmarkhistory',
            name='updated_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='trialtesthistory',
            name='updated_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='trialtestmark',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 12, 19, 14, 44, 590449)),
        ),
        migrations.AlterField(
            model_name='trialtestmarkhistory',
            name='updated_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]