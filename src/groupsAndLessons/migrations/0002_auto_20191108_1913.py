# Generated by Django 2.1 on 2019-11-08 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('groupsAndLessons', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lessongroupstudenthistory',
            old_name='lesson_group_id',
            new_name='schedule_id',
        ),
        migrations.RemoveField(
            model_name='lessongroupstudent',
            name='lesson_group',
        ),
        migrations.AddField(
            model_name='lessongroupstudent',
            name='schedule',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='groupsAndLessons.Schedule'),
            preserve_default=False,
        ),
    ]
