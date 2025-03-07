# Generated by Django 5.1.4 on 2025-01-28 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0002_remove_gender_id_remove_role_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Heamophilia',
            fields=[
                ('heamophilia_id', models.CharField(editable=False, max_length=3, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
