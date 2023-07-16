from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Elevator, Request
from ..serializers import ElevatorSerializer, RequestSerializer
from django.db import transaction

class CurrentDirectionView(APIView):
    def get(self, request, elevator_id):
        try:
            elevator = Elevator.objects.get(id=elevator_id)
        except Elevator.DoesNotExist:
            return Response({'error': 'Elevator does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        if elevator.is_operational == False:
            return Response({'error': 'Elevator in Maintenance.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'current_direction': elevator.current_direction})

    # Explanation: API endpoint for fetching the current direction of a specific elevator.
    # It retrieves the elevator based on the provided elevator_id and returns the current_direction field.
    # If the elevator does not exist or is in maintenance mode, an appropriate error response is returned.


def get_floor(elevator):
    requests = elevator.requests.filter(status='PENDING')
    
    # If there are no pending requests, set the elevator's current_direction to "IDLE" and return
    if not requests:
        elevator.current_direction = "IDLE"
        elevator.save()
        return
    
    current_floor = elevator.current_floor
    current_direction = elevator.current_direction
    
    if current_direction == "UP":
        # If the current_direction is "UP", try to find the next destination floor above the current floor
        next_destination = requests.filter(floor__gt=current_floor).order_by('floor').first()
        
        if next_destination:
            return next_destination
        else:
            # If there are no pending requests above the current floor, switch the direction to "DOWN"
            next_destination = requests.filter(floor__lt=current_floor).order_by('-floor').first()
            
            if next_destination:
                elevator.current_direction = "DOWN"
                elevator.save()
                return next_destination
    else:
        # If the current_direction is "DOWN", try to find the next destination floor below the current floor
        next_destination = requests.filter(floor__lt=current_floor+1).order_by('-floor').first()
        
        if next_destination:
            return next_destination
        else:
            # If there are no pending requests below the current floor, switch the direction to "UP"
            next_destination = requests.filter(floor__gt=current_floor).order_by('floor').first()
    
            if next_destination:
                elevator.current_direction = "UP"
                elevator.save()
                return next_destination
    
    return None


class NextDestinationView(APIView):
    def get(self, request, elevator_id):
        try:
            elevator = Elevator.objects.get(id=elevator_id)
        except Elevator.DoesNotExist:
            return Response({'error': 'Elevator does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        if elevator.is_operational == False:
            return Response({'error': 'Elevator in Maintenance.'}, status=status.HTTP_404_NOT_FOUND)

        next_destination = get_floor(elevator)
        
        # If there is no next destination available, return the current floor as the next destination
        if next_destination is None:
            return Response({'next_destination': elevator.current_floor})

        return Response({'next_destination': next_destination.floor})

    # Explanation: API endpoint for fetching the next destination floor for a given elevator.
    # It retrieves the elevator based on the provided elevator_id.
    # If the elevator does not exist or is in maintenance mode, an appropriate error response is returned.
    # It then calls the get_floor function to calculate the next destination floor based on the elevator's current direction and pending requests.
    # If there is no next destination available, the current floor is returned as the next destination.

    

class SetElevatorDoorView(APIView):
    def post(self, request, elevator_id):
        try:
            elevator = Elevator.objects.get(id=elevator_id)
        except Elevator.DoesNotExist:
            return Response({'error': 'Elevator does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        if elevator.is_operational == False:
            return Response({'error': 'Elevator in Maintenance.'}, status=status.HTTP_404_NOT_FOUND)

        action = request.data.get('action')

        if action == 'open':
            # Set the elevator door to open
            elevator.is_open = True
            elevator.save()
            return Response({'status': 'Success'}, status=status.HTTP_200_OK)
        elif action == 'close':
            # Check if there is a next destination floor
            next_destination = get_floor(elevator)
            
            if next_destination == None:
                # If there is no next destination, close the elevator door
                elevator.is_open = False
                elevator.save()
            else:
                # If there is a next destination, update the elevator and request objects in a transaction
                with transaction.atomic():
                    next_destination.status = 'COMPLETED'
                    next_destination.save()
                    elevator.current_floor = next_destination.floor
                    elevator.is_open = True
                    elevator.save()
            
            return Response({'status': 'Success'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

    # Explanation: API endpoint for opening and closing the elevator door.
    # It retrieves the elevator based on the provided elevator_id.
    # If the elevator does not exist or is in maintenance mode, an appropriate error response is returned.
    # It checks the requested action ('open' or 'close') and performs the corresponding operation on the elevator.
    # If the action is 'open', it sets the elevator door to open.
    # If the action is 'close', it checks if there is a next destination floor.
    # If there is no next destination, it closes the elevator door.
    # If there is a next destination, it updates the elevator and request objects in a transaction.
    # The next destination request is marked as 'COMPLETED', the elevator's current floor is updated, and the elevator door is set to open.
