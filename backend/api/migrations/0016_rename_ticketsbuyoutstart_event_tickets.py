# Generated by Django 3.2.16 on 2022-11-10 22:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0015_event_ticketsbuyoutstart"),
    ]

    operations = [
        migrations.RenameField(
            model_name="event",
            old_name="ticketsBuyoutStart",
            new_name="tickets",
        ),
    ]