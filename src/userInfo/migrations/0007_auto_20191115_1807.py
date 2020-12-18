# Generated by Django 2.1 on 2019-11-15 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userInfo', '0006_parent_parenthistory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='gold_medal',
        ),
        migrations.RemoveField(
            model_name='student',
            name='red_medal',
        ),
        migrations.RemoveField(
            model_name='studenthistory',
            name='gold_medal',
        ),
        migrations.RemoveField(
            model_name='studenthistory',
            name='red_medal',
        ),
        migrations.AddField(
            model_name='student',
            name='certificate',
            field=models.CharField(choices=[('B', 'Blue'), ('R', 'Red'), ('G', 'Gold')], default='B', max_length=1),
        ),
        migrations.AddField(
            model_name='studenthistory',
            name='certificate',
            field=models.CharField(default='B', max_length=1),
        ),
    ]
