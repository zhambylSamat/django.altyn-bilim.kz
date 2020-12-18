# Generated by Django 2.1 on 2019-11-08 10:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('materials', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LessonGroupIpConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_checking_ip', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LessonGroupIpConfigurationHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin_id', models.IntegerField()),
                ('user_id', models.IntegerField()),
                ('is_checking_ip', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField()),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-updated_date'],
            },
        ),
        migrations.CreateModel(
            name='SubjectQuizConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_practice', models.BooleanField(default=False)),
                ('is_theory', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='materials.Subject')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_date'],
            },
        ),
        migrations.CreateModel(
            name='SubjectQuizConfigurationHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin_id', models.IntegerField()),
                ('user_id', models.IntegerField()),
                ('subject_id', models.IntegerField()),
                ('is_practice', models.BooleanField(default=False)),
                ('is_theory', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField()),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-updated_date'],
            },
        ),
        migrations.CreateModel(
            name='TrialTestMaxMarkConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_val', models.IntegerField()),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='materials.Subject')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['subject'],
            },
        ),
        migrations.CreateModel(
            name='TrialTestMaxMarkConfigurationHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin_id', models.IntegerField()),
                ('user_id', models.IntegerField()),
                ('subject_id', models.IntegerField()),
                ('max_val', models.IntegerField()),
                ('created_date', models.DateTimeField()),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-updated_date'],
            },
        ),
        migrations.CreateModel(
            name='TrialTestMinMarkConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_val', models.IntegerField()),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='materials.Subject')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_date'],
            },
        ),
        migrations.CreateModel(
            name='TrialTestMinMarkConfigurationHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin_id', models.IntegerField()),
                ('user_id', models.IntegerField()),
                ('subject_id', models.IntegerField()),
                ('min_val', models.IntegerField()),
                ('created_date', models.DateTimeField()),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-created_date'],
            },
        ),
    ]