import uuid
from django.db import models

class Elevator(models.Model):
    DIRECTION_CHOICES = [
        ('UP', 'Up'),
        ('DOWN', 'Down'),
        ('IDLE', 'Idle'),
    ]
    current_direction = models.CharField(max_length=5, choices=DIRECTION_CHOICES, default='IDLE')
    is_operational = models.BooleanField(default=True)
    current_floor = models.PositiveIntegerField(default=0)
    is_open = models.BooleanField(default=False)

class Request(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    elevator = models.ForeignKey(Elevator, on_delete=models.CASCADE, related_name='requests', default=0)
    floor = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')



