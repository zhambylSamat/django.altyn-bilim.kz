# Generated by Django 2.1 on 2020-02-29 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0005_auto_20200229_1831'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trialtestmarkconfiguration',
            old_name='min_mark',
            new_name='bad_mark',
        ),
        migrations.RenameField(
            model_name='trialtestmarkconfigurationhistory',
            old_name='min_mark',
            new_name='bad_mark',
        ),
        migrations.AddField(
            model_name='trialtestmarkconfiguration',
            name='good_mark',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trialtestmarkconfigurationhistory',
            name='good_mark',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
