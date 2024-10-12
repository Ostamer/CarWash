# Generated by Django 5.1 on 2024-08-29 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wash_car', '0006_alter_carwashworktime_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carwashworktime',
            name='day',
            field=models.TextField(choices=[('mon', 'Понедельник'), ('tue', 'Вторник'), ('wen', 'Среда'), ('thu', 'Четверг'), ('fri', 'Пятница'), ('sat', 'Суббота'), ('sun', 'Воскресенье')], max_length=3),
        ),
    ]
