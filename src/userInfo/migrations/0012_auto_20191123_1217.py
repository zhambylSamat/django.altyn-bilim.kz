# Generated by Django 2.1 on 2019-11-23 06:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userInfo', '0011_auto_20191123_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parent',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='student_parent', to='userInfo.Student'),
        ),
    ]