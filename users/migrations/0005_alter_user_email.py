# Generated by Django 3.2 on 2023-08-09 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(blank=True, max_length=30, null=True, unique=True, verbose_name='email address'),
        ),
    ]