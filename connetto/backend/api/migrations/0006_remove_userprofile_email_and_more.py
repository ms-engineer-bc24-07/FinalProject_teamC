# Generated by Django 5.1.3 on 2024-12-18 15:41

import datetime

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0005_merge_20241218_1536"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="email",
        ),
        migrations.AlterField(
            model_name="participation",
            name="desired_dates",
            field=models.JSONField(
                validators=[
                    django.core.validators.MinValueValidator(
                        datetime.date(2024, 12, 18)
                    )
                ]
            ),
        ),
        migrations.AlterField(
            model_name="participation",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="participations",
                to="api.userprofile",
            ),
        ),
    ]
