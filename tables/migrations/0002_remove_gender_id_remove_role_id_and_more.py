# Generated by Django 5.1.4 on 2025-01-21 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gender',
            name='id',
        ),
        migrations.RemoveField(
            model_name='role',
            name='id',
        ),
        migrations.AlterField(
            model_name='gender',
            name='gender_id',
            field=models.CharField(editable=False, max_length=3, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='role',
            name='role_id',
            field=models.CharField(editable=False, max_length=3, primary_key=True, serialize=False),
        ),
    ]
