# Generated by Django 3.2.16 on 2022-12-02 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0015_auto_20221129_2001"),
    ]

    operations = [
        migrations.AlterField(
            model_name="perk",
            name="tooltip",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
