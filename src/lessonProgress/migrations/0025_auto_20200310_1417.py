# Generated by Django 2.1 on 2020-03-10 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessonProgress', '0024_auto_20200310_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topicquizmarkhistory',
            name='changed_user_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
