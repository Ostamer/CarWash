# Generated by Django 5.1 on 2024-08-28 13:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wash_car', '0004_rename_user_washrecord_client_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carwash',
            name='work_hours',
        ),
    ]