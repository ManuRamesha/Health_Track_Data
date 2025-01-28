# Generated by Django 5.1.4 on 2025-01-28 12:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ka_regd_no', models.CharField(max_length=20, unique=True)),
                ('heamophilia_type', models.CharField(blank=True, max_length=20, null=True)),
                ('percentage', models.CharField(blank=True, choices=[('1-10%', '1-10%'), ('10-20%', '10-20%'), ('20-30%', '20-30%'), ('30-40%', '30-40%'), ('40-50%', '40-50%'), ('50-60%', '50-60%'), ('60-70%', '60-70%'), ('70-80%', '70-80%'), ('80-90%', '80-90%'), ('90-100%', '90-100%'), ('less then 1%', 'less then 1%')], max_length=20, null=True)),
                ('factor', models.CharField(blank=True, choices=[('vii', 'vii'), ('viii', 'viii'), ('ix', 'ix'), ('xi', 'xi')], max_length=20, null=True)),
                ('inhibitor', models.CharField(blank=True, choices=[('yes', 'YES'), ('no', 'NO')], max_length=20, null=True)),
                ('inhibitor_percentage', models.FloatField(blank=True, null=True)),
                ('target_joints', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
