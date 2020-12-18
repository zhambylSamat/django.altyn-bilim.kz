# Generated by Django 2.1 on 2020-01-31 14:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0004_auto_20191207_1413'),
        ('groupsAndLessons', '0036_auto_20200131_1859'),
        ('lessonProgress', '0007_auto_20200130_1752'),
    ]

    operations = [
        migrations.CreateModel(
            name='LessonTestAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('lesson_group_student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='groupsAndLessons.LessonGroupStudent')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materials.TopicTest')),
            ],
            options={
                'ordering': ['-created_date'],
            },
        ),
        migrations.CreateModel(
            name='LessonTestActionHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin_id', models.IntegerField()),
                ('changed_user_id', models.IntegerField(blank=True, null=True)),
                ('lesson_group_student', models.IntegerField()),
                ('test_id', models.IntegerField()),
                ('created_date', models.DateTimeField()),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-updated_date'],
            },
        ),
        migrations.CreateModel(
            name='LessonVideoAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('lesson_group_student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='groupsAndLessons.LessonGroupStudent')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materials.Video')),
            ],
            options={
                'ordering': ['-created_date'],
            },
        ),
        migrations.CreateModel(
            name='LessonVideoActionHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin_id', models.IntegerField()),
                ('changed_user_id', models.IntegerField(blank=True, null=True)),
                ('lesson_group_student', models.IntegerField()),
                ('video_id', models.IntegerField()),
                ('created_date', models.DateTimeField()),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-updated_date'],
            },
        ),
        migrations.RemoveField(
            model_name='lessonaction',
            name='lesson_group_student',
        ),
        migrations.RemoveField(
            model_name='lessonaction',
            name='user',
        ),
        migrations.DeleteModel(
            name='LessonActionHistory',
        ),
        migrations.DeleteModel(
            name='LessonAction',
        ),
    ]