# Generated by Django 2.1 on 2020-02-06 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subjectquizconfiguration',
            name='user',
        ),
        migrations.RemoveField(
            model_name='subjectquizconfigurationhistory',
            name='user_id',
        ),
        migrations.AddField(
            model_name='subjectquizconfigurationhistory',
            name='changed_user_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
