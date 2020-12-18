# Generated by Django 2.1 on 2020-03-12 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userInfo', '0032_studentgroupfreeze_studentgroupfreezehistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parent',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='parenthistory',
            name='updated_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='staffhistory',
            name='updated_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='studentfreeze',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='studentfreezehistory',
            name='updated_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='studentgroupfreezehistory',
            name='updated_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='studenthistory',
            name='updated_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='userrolehistory',
            name='updated_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
