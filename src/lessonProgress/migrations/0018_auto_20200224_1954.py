# Generated by Django 2.1 on 2020-02-24 13:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0005_auto_20200224_1950'),
        ('lessonProgress', '0017_auto_20200222_1630'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lessonvideoactionhistory',
            old_name='video_id',
            new_name='topic_id',
        ),
        migrations.RemoveField(
            model_name='lessonvideoaction',
            name='video',
        ),
        migrations.AddField(
            model_name='lessonvideoaction',
            name='topic',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='materials.Topic'),
            preserve_default=False,
        ),
    ]
