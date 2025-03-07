# Generated by Django 5.1.4 on 2025-02-04 12:06

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyTrack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('break_through_bleed', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10)),
                ('break_through_bleed_details', models.TextField(blank=True, null=True)),
                ('treatment_for_bleed', models.TextField(blank=True, null=True)),
                ('inj_hemilibra', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10)),
                ('physiotherapy', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dailytrack', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
