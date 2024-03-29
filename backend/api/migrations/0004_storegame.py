# Generated by Django 3.1.5 on 2021-03-15 22:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_location_type"),
    ]

    operations = [
        migrations.CreateModel(
            name="StoreGame",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("selling_price", models.FloatField(default=0.0)),
                ("selling_price_associate", models.FloatField(default=0.0)),
                ("buying_price", models.FloatField(default=0.0)),
                ("stock", models.FloatField(default=0.0)),
                (
                    "game",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.bgggame",
                    ),
                ),
                (
                    "supplier",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.supplier",
                    ),
                ),
            ],
        ),
    ]
