# Generated by Django 3.1.5 on 2021-02-27 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210210_1622'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='type',
            field=models.CharField(choices=[('room', 'Room'), ('shelf', 'Shelf')], default='shelf', max_length=32),
        ),
    ]
