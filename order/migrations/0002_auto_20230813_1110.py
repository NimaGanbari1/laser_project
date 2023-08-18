# Generated by Django 3.2 on 2023-08-13 07:40

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='ProductCode',
        ),
        migrations.RemoveField(
            model_name='order',
            name='ProductCount',
        ),
        migrations.AddField(
            model_name='order',
            name='ProductCodes',
            field=django_mysql.models.ListCharField(models.CharField(max_length=7, verbose_name='code'), default=None, max_length=130, size=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='ProductCounts',
            field=django_mysql.models.ListCharField(models.CharField(max_length=4, verbose_name='count'), default=1, max_length=90, size=15),
            preserve_default=False,
        ),
    ]