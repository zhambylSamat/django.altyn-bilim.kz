# Generated by Django 2.1 on 2019-12-07 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groupsAndLessons', '0006_auto_20191127_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentplanhistory',
            name='changed_user_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='topicplanhistory',
            name='changed_user_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
