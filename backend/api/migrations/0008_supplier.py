# Generated by Django 3.1.4 on 2020-12-17 18:26

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20201120_1017'),
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, default=None, max_length=128, null=True, region=None)),
                ('email', models.EmailField(blank=True, default=None, max_length=254, null=True)),
                ('website', models.EmailField(blank=True, default=None, max_length=254, null=True)),
            ],
        ),
    ]