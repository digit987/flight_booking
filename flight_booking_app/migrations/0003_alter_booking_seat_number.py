# Generated by Django 5.0.2 on 2024-02-25 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight_booking_app', '0002_booking_seat_number_alter_flight_flight_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='seat_number',
            field=models.CharField(default=1, max_length=60),
        ),
    ]