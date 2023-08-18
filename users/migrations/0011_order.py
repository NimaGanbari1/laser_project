# Generated by Django 3.2 on 2023-08-13 07:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_cart_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ProductCode', models.IntegerField()),
                ('ProductCount', models.IntegerField()),
                ('Price', models.BigIntegerField()),
                ('Address', models.TextField()),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='create time')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='update time')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Orders', to='users.user')),
            ],
        ),
    ]