# Generated by Django 3.1.6 on 2021-02-26 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0004_auto_20210225_2302'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='education',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='experience',
            name='duration',
        ),
        migrations.AddField(
            model_name='education',
            name='start',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='experience',
            name='start',
            field=models.DateField(null=True),
        ),
    ]
