# Generated by Django 2.1 on 2020-02-18 13:38

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userInfo', '0027_auto_20200118_2021'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostTeacherSalary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('infos', django.contrib.postgres.fields.jsonb.JSONField()),
                ('created_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PostTeacherSalaryHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin_id', models.IntegerField()),
                ('changed_user_id', models.IntegerField(blank=True, null=True)),
                ('infos', django.contrib.postgres.fields.jsonb.JSONField()),
                ('created_date', models.DateTimeField()),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-updated_date'],
            },
        ),
        migrations.CreateModel(
            name='PreTeacherSalary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('infos', django.contrib.postgres.fields.jsonb.JSONField()),
                ('created_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PreTeacherSalaryHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin_id', models.IntegerField()),
                ('changed_user_id', models.IntegerField(blank=True, null=True)),
                ('infos', django.contrib.postgres.fields.jsonb.JSONField()),
                ('created_date', models.DateTimeField()),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-updated_date'],
            },
        ),
        migrations.CreateModel(
            name='TeacherCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userInfo.Staff')),
            ],
        ),
        migrations.CreateModel(
            name='TeacherCategoryHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin_id', models.IntegerField()),
                ('changed_user_id', models.IntegerField()),
                ('teacher_salary_category_id', models.IntegerField()),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='TeacherSalaryCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=120)),
                ('lessons_per_week', models.IntegerField()),
                ('created_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TeacherSalaryCategoryHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin_id', models.IntegerField()),
                ('changed_user_id', models.IntegerField()),
                ('category', models.CharField(max_length=120)),
                ('lessons_per_week', models.IntegerField()),
                ('created_date', models.DateTimeField()),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-updated_date'],
            },
        ),
        migrations.CreateModel(
            name='TeacherSalaryCoefficient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coefficient', models.DecimalField(decimal_places=1, max_digits=2)),
                ('price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('teacher_salary_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.TeacherSalaryCategory')),
            ],
        ),
        migrations.CreateModel(
            name='TeacherSalaryCoefficientHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin_id', models.IntegerField()),
                ('changed_user_id', models.IntegerField()),
                ('teacher_salary_category_id', models.IntegerField()),
                ('coefficient', models.DecimalField(decimal_places=1, max_digits=2)),
                ('price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-updated_date'],
            },
        ),
        migrations.CreateModel(
            name='TeacherSalaryFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.TextField()),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('post_teacher_salary', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='payment.PostTeacherSalary')),
            ],
        ),
        migrations.AddField(
            model_name='teachercategory',
            name='teacher_salary_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='payment.TeacherSalaryCategory'),
        ),
    ]
