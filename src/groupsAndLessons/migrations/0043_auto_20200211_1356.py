# Generated by Django 2.1 on 2020-02-11 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groupsAndLessons', '0042_auto_20200207_1929'),
    ]

    operations = [
        migrations.CreateModel(
            name='DayOff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('comment', models.TextField()),
                ('created_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='DayOffHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin_id', models.IntegerField()),
                ('changed_user_id', models.IntegerField(blank=True, null=True)),
                ('date', models.DateField()),
                ('comment', models.TextField()),
                ('created_date', models.DateTimeField()),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-updated_date'],
            },
        ),
        migrations.AlterModelOptions(
            name='lessongroupstudentshortschedulehistory',
            options={'ordering': ['-updated_date']},
        ),
    ]