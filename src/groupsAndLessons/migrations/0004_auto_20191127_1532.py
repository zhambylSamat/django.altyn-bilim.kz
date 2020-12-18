# Generated by Django 2.1 on 2019-11-27 09:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0001_initial'),
        ('groupsAndLessons', '0003_auto_20191113_1729'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopicPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(max_length=3)),
                ('topic_progress', models.DecimalField(decimal_places=1, max_digits=2)),
                ('created_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-student_plan'],
            },
        ),
        migrations.CreateModel(
            name='TopicPlanHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin_id', models.IntegerField()),
                ('student_plan_id', models.IntegerField()),
                ('topic_id', models.IntegerField()),
                ('order', models.IntegerField(max_length=3)),
                ('topic_progress', models.DecimalField(decimal_places=1, max_digits=2)),
                ('created_date', models.DateTimeField()),
                ('updated_date', models.DateTimeField()),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-updated_date'],
            },
        ),
        migrations.RemoveField(
            model_name='studentplan',
            name='plan_json',
        ),
        migrations.RemoveField(
            model_name='studentplanhistory',
            name='plan_json',
        ),
        migrations.AddField(
            model_name='topicplan',
            name='student_plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='groupsAndLessons.StudentPlan'),
        ),
        migrations.AddField(
            model_name='topicplan',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='materials.Topic'),
        ),
    ]