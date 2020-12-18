# Generated by Django 2.1 on 2020-02-22 10:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('groupsAndLessons', '0047_auto_20200222_1546'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('lesson_group', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='lg_group_schedule', to='groupsAndLessons.LessonGroup')),
            ],
        ),
        migrations.CreateModel(
            name='GroupScheduleHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin_id', models.IntegerField()),
                ('changed_user_id', models.IntegerField(blank=True, null=True)),
                ('lesson_group_id', models.IntegerField()),
                ('created_date', models.DateTimeField()),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-updated_date'],
            },
        ),
        migrations.AlterField(
            model_name='grouptimetransfer',
            name='lesson_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lg_group_time_transfer', to='groupsAndLessons.LessonGroup'),
        ),
        migrations.AlterField(
            model_name='materialaccessinfo',
            name='lesson_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='lg_material_access_info', to='groupsAndLessons.LessonGroup'),
        ),
    ]
