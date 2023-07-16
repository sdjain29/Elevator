from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Elevator, Request
from ..serializers import RequestSerializer
from django.db import transaction
from .direction import get_floor

class SaveUserInternalRequestView(APIView):
    def post(self, request, elevator_id):
        try:
            elevator = Elevator.objects.get(id=elevator_id)
        except Elevator.DoesNotExist:
            return Response({'error': 'Elevator does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        if elevator.is_operational == False:
            return Response({'error': 'Elevator in Maintenance.'}, status=status.HTTP_404_NOT_FOUND)

        requested_floor = request.data.get('floor')
        
        # Call the elevator_trigger function to handle the user's internal request
        return elevator_trigger(elevator, requested_floor)

    # Explanation: API endpoint for saving a user's internal request for a specific elevator.
    # It retrieves the elevator based on the provided elevator_id.
    # If the elevator does not exist or is in maintenance mode, an appropriate error response is returned.
    # It retrieves the requested floor from the request data.
    # Then, it calls the elevator_trigger function to handle the user's internal request.
    # The elevator_trigger function will determine the next step for elevator to handle the request and trigger the necessary actions.

    
class SaveUserExternalRequestView(APIView):
   
    # Below Function Explanation: Method to find the most optimal elevator for a requested floor.
    # It takes the requested floor as input.
    # It retrieves all elevators that are operational.
    # If there are no operational elevators, it returns None.
    # It initializes the optimal_elevator variable as the first elevator in the list.
    # It sets an initial min_distance value as a large number.
    # It iterates through each elevator to calculate the distance and find the elevator with the minimum distance.
    # For each elevator, it considers the current floor, current direction, and the requested floor.
    # It calculates the distance based on the elevator's current direction and the relationship between the current floor and the requested floor.
    # If a shorter distance is found, it updates the optimal_elevator and min_distance values.
    # Finally, it returns the most optimal elevator based on the calculated distances.

    def get_elevator(self, requested_floor):
        elevators = Elevator.objects.filter(is_operational=True)

        optimal_elevator = None
        if len(elevators) == 0:
            return optimal_elevator

        optimal_elevator = elevators[0]
        min_distance = 10000

        for elevator in elevators:
            current_floor = elevator.current_floor
            current_direction = elevator.current_direction

            if current_direction == 'IDLE':
                # If the elevator is idle, calculate the distance as the absolute difference between the requested floor and the current floor
                distance = abs(requested_floor - current_floor)
            elif current_direction == 'UP':
                if current_floor > requested_floor:
                    # If the elevator is moving up and the current floor is above the requested floor, calculate the distance as the difference between the current floor and the requested floor
                    distance = current_floor - requested_floor
                else:
                    # If the elevator is moving up and the current floor is below the requested floor, calculate the distance considering the maximum requested floor in the upward direction
                    max_requested_floor = elevator.requests.filter(status='PENDING', floor__gt=current_floor).order_by('-floor').first()
                    if max_requested_floor:
                        distance = max_requested_floor.floor - current_floor + max_requested_floor.floor - requested_floor
                    else:
                        distance = current_floor - requested_floor
            else:
                if current_floor < requested_floor:
                    # If the elevator is moving down and the current floor is below the requested floor, calculate the distance as the difference between the requested floor and the current floor
                    distance = requested_floor - current_floor
                else:
                    # If the elevator is moving down and the current floor is above the requested floor, calculate the distance considering the maximum requested floor in the downward direction
                    max_requested_floor = elevator.requests.filter(status='PENDING', floor__lt=current_floor).order_by('floor').first()
                    if max_requested_floor:
                        distance = current_floor - max_requested_floor.floor + requested_floor - max_requested_floor.floor
                    else:
                        distance = requested_floor - current_floor

            if distance < min_distance:
                min_distance = distance
                optimal_elevator = elevator
                return optimal_elevator

    
    def post(self, request):
        requested_floor = request.data.get('floor')
        elevator = self.get_elevator(requested_floor)
        if elevator is None:
            return Response({'error': 'No available elevators or elevator is under maintenance.'}, status=status.HTTP_404_NOT_FOUND)
        return elevator_trigger(elevator, requested_floor)

    # Explanation: Method to handle the user's request to call an elevator for a specific floor.
    # It takes the HTTP request object as input.
    # It extracts the requested floor from the request data.
    # It then calls the get_elevator method to find the most optimal elevator for the requested floor.
    # If there is no available elevator or if the elevator is under maintenance, it returns an error response.
    # If an elevator is available, it triggers the elevator actions for the requested floor by calling the elevator_trigger method.
    # Finally, it returns the response generated by the elevator_trigger method.




def elevator_trigger(elevator, requested_floor):
    # Check if there is a pending request for the same floor
    requests = elevator.requests.filter(status='PENDING', floor=requested_floor)
    if len(requests) != 0:
        # If a request for the same floor already exists, return its details
        serializer = RequestSerializer(requests[0])
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Check if there are any other pending requests
    requests = elevator.requests.filter(status='PENDING')
    request_obj = Request.objects.create(elevator=elevator, floor=requested_floor)

    if elevator.is_open == True:
        # If the elevator door is open
        if len(requests) == 0:
            # If there are no other pending requests, update the elevator's current direction based on the requested floor
            if elevator.current_floor > requested_floor:
                elevator.current_direction = "DOWN"
            else:
                elevator.current_direction = "UP"
            elevator.save()
    else:
        # If the elevator door is closed
        if len(requests) == 0:
            # If there are no other pending requests, update the elevator's current floor, open the door, and mark the request as completed
            with transaction.atomic():
                request_obj.status = 'COMPLETED'
                request_obj.save()
                elevator.current_floor = requested_floor
                elevator.is_open = True
                elevator.save()

    # Trigger the process to determine the next destination floor
    get_floor(elevator)

    # Serialize the created request object
    serializer = RequestSerializer(request_obj)
    return Response(serializer.data, status=status.HTTP_201_CREATED)