# Generated by Django 5.1.4 on 2025-01-21 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_user_age_alter_user_is_active_alter_user_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='user',
            name='role',
        ),
    ]
