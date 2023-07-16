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

    # Explanation: Represents the current direction of the elevator.
    # Choices: 'UP', 'DOWN', 'IDLE'
    # Default: 'IDLE'

    # Explanation: Indicates whether the elevator is operational or not.
    # Default: True (Assuming the elevator is operational by default)

    # Explanation: Represents the current floor where the elevator is located.
    # Default: 0 (Assuming the elevator starts at the ground floor)

    # Explanation: Indicates whether the elevator doors are open or closed.
    # Default: False (Assuming the doors are closed initially)


class Request(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    elevator = models.ForeignKey(Elevator, on_delete=models.CASCADE, related_name='requests', default=0)
    floor = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    # Explanation: Represents the associated elevator for the request.
    # Relationship: Many-to-One (An elevator can have multiple requests)
    # Default: 0 (Assuming a default elevator value for requests)

    # Explanation: Represents the floor for which the request is made.
    # Note: This assumes that the floors are represented by positive integers.

    # Explanation: Indicates the status of the request.
    # Choices: 'PENDING', 'COMPLETED', 'CANCELLED'
    # Default: 'PENDING' (Assuming the request is initially pending)
