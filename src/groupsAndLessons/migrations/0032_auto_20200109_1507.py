# Generated by Django 2.1 on 2020-01-09 09:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('groupsAndLessons', '0031_auto_20191230_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessongroupstudent',
            name='lesson_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='lesson_group_plan', to='groupsAndLessons.LessonGroup'),
        ),
    ]
