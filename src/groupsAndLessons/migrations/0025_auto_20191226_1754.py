# Generated by Django 2.1 on 2019-12-26 11:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('groupsAndLessons', '0024_auto_20191226_1734'),
    ]

    operations = [
        migrations.CreateModel(
            name='LessonGroupSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='LessonGroupScheduleHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin_id', models.IntegerField()),
                ('changed_user_id', models.IntegerField(blank=True, null=True)),
                ('schedule_id', models.IntegerField()),
                ('lesson_group_id', models.IntegerField()),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='lessongroup',
            name='schedule',
        ),
        migrations.RemoveField(
            model_name='lessongrouphistory',
            name='schedule_ids',
        ),
        migrations.AddField(
            model_name='lessongroupschedule',
            name='lesson_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='groupsAndLessons.LessonGroup'),
        ),
        migrations.AddField(
            model_name='lessongroupschedule',
            name='schedule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='groupsAndLessons.Schedule'),
        ),
    ]
