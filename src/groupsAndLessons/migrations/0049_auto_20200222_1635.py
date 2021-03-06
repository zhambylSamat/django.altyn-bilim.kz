# Generated by Django 2.1 on 2020-02-22 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('groupsAndLessons', '0048_auto_20200222_1632'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lessongroupschedulehistory',
            old_name='lesson_group_id',
            new_name='group_schedule_id',
        ),
        migrations.RemoveField(
            model_name='lessongroupschedule',
            name='lesson_group',
        ),
        migrations.AddField(
            model_name='lessongroupschedule',
            name='group_schedule',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='gs_lesson_group_schedule', to='groupsAndLessons.GroupSchedule'),
            preserve_default=False,
        ),
    ]
