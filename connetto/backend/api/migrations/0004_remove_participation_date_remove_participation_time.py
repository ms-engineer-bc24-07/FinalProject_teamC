# Generated by Django 5.1.3 on 2024-12-18 15:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_alter_participation_date_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="participation",
            name="date",
        ),
        migrations.RemoveField(
            model_name="participation",
            name="time",
        ),
    ]
