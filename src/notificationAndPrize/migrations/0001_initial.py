# Generated by Django 2.1 on 2020-02-29 13:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chocolate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_got', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_got', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(choices=[('2DA', '2 рет қатарынан сабаққа келмеді'), ('RRQ', 'Пересдачадан құлады'), ('3UTT', '3 рет баллын көтерді'), ('MTT', 'Пробный тесттен макс. жинады'), ('MQ', 'Аралық бақылаудан макс. жинады'), ('EQ', 'Аралық бақылауды жақсы жазды')], max_length=10)),
                ('notification_class', models.CharField(choices=[('S', 'success'), ('W', 'warning'), ('D', 'danger')], max_length=1)),
                ('object_id', models.IntegerField()),
                ('is_shown', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='discount',
            name='notification',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='notificationAndPrize.Notification'),
        ),
        migrations.AddField(
            model_name='discount',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chocolate',
            name='notification',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='notificationAndPrize.Notification'),
        ),
        migrations.AddField(
            model_name='chocolate',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
