# Generated by Django 2.1 on 2019-12-05 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0002_auto_20191205_1915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topichistory',
            name='parent_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='topichistory',
            name='subject_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
