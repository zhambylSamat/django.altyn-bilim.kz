# Generated by Django 2.1 on 2020-02-26 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groupsAndLessons', '0051_auto_20200222_1856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materialaccessinfo',
            name='accessed_ipv4',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='materialaccessinfo',
            name='accessed_ipv6',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='materialaccessinfohistory',
            name='accessed_ipv4',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='materialaccessinfohistory',
            name='accessed_ipv6',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
