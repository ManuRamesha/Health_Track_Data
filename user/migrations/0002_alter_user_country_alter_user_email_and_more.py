# Generated by Django 5.1.4 on 2025-01-20 06:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='country',
            field=models.CharField(blank=True, default='India', editable=False, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='parent_phone_number',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+91xxxxxxxxxx'. Up to 13 digits allowed.", regex='^\\+?(91?|0?)[6789]\\d{9}$')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+91xxxxxxxxxx'. Up to 13 digits allowed.", regex='^\\+?(91?|0?)[6789]\\d{9}$')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='zip_code',
            field=models.CharField(blank=True, max_length=6, null=True, validators=[django.core.validators.RegexValidator(message="Zip code must be entered in the format: 'xxxxxx'. Up to 6 digits allowed.", regex='^[1-9][0-9]{5}$')]),
        ),
    ]
