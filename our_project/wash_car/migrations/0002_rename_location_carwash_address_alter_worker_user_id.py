# Generated by Django 5.1 on 2024-08-28 09:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wash_car', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='carwash',
            old_name='location',
            new_name='address',
        ),
        migrations.AlterField(
            model_name='worker',
            name='user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='wash_car.user'),
        ),
    ]
