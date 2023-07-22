# Generated by Django 3.2 on 2023-07-19 17:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.BigIntegerField(blank=True, error_messages={'unique': 'A user with that phone number already exists.'}, null=True, unique=True, validators=[django.core.validators.RegexValidator('^989[0-3,9]\\d{8}$', 'Enter a valid number phone', 'invalid')], verbose_name='phone number'),
        ),
    ]
