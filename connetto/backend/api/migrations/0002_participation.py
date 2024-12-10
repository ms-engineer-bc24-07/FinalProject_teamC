# Generated by Django 5.1.3 on 2024-12-07 04:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Participation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender_restriction', models.CharField(choices=[('same_gender', '同性'), ('no_restriction', '希望なし')], default='no_restriction', max_length=50)),
                ('age_restriction', models.CharField(choices=[('same_age', '同年代'), ('broad_age', '幅広い年代'), ('no_restriction', '希望なし')], default='no_restriction', max_length=50)),
                ('joining_year_restriction', models.CharField(choices=[('exact_match', '完全一致'), ('no_restriction', '希望なし')], default='no_restriction', max_length=50)),
                ('department_restriction', models.CharField(choices=[('same_department', '所属部署内希望'), ('mixed_departments', '他部署混在'), ('no_restriction', '希望なし')], default='no_restriction', max_length=50)),
                ('atmosphere_preference', models.CharField(choices=[('quiet', '落ち着いたお店'), ('lively', 'わいわいできるお店'), ('no_restriction', '希望なし')], default='no_restriction', max_length=50)),
                ('desired_dates', models.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
