# Generated by Django 4.2.3 on 2023-07-16 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elevator_system', '0006_remove_elevator_requests_request_elevator'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('COMPLETED', 'Completed'), ('CANCELLED', 'Cancelled')], default='PENDING', max_length=10),
        ),
    ]