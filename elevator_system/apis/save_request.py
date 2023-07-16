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
            return Response({'error': 'Elevator in Maintainance.'}, status=status.HTTP_404_NOT_FOUND)

        requested_floor = request.data.get('floor')
        return elevator_trigger(elevator, requested_floor)

    
class SaveUserExternalRequestView(APIView):
    def get_elevator(self, requested_floor):
        elevators = Elevator.objects.filter(is_operational=True)

        optimal_elevator = None
        if len(elevators)==0:
            return optimal_elevator
        
        optimal_elevator = elevators[0]
        min_distance = 10000

        for elevator in elevators:
            current_floor = elevator.current_floor
            current_direction = elevator.current_direction

            if current_direction == 'IDLE':
                distance = abs(requested_floor - current_floor)
            elif current_direction == 'UP':
                if current_floor > requested_floor:
                    distance = current_floor - requested_floor
                else:
                    max_requested_floor = elevator.requests.filter(status='PENDING', floor__gt=current_floor).order_by('-floor').first()
                    if max_requested_floor:
                        distance = max_requested_floor.floor - current_floor + max_requested_floor.floor - requested_floor
                    else:
                        distance = current_floor - requested_floor
            else:
                if current_floor < requested_floor:
                    distance = requested_floor - current_floor
                else:
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



def elevator_trigger(elevator, requested_floor):
    requests = elevator.requests.filter(status='PENDING', floor=requested_floor)
    if len(requests) != 0:
        serializer = RequestSerializer(requests[0])
        return Response(serializer.data, status=status.HTTP_200_OK)


    requests = elevator.requests.filter(status='PENDING')
    request_obj = Request.objects.create(elevator=elevator, floor=requested_floor)

    if elevator.is_open == True:
        if len(requests) == 0:
            if elevator.current_floor > requested_floor:
                elevator.current_direction = "DOWN"
            else:
                elevator.current_direction = "UP"
            elevator.save()
    else:
        if len(requests) == 0:
            with transaction.atomic():
                request_obj.status = 'COMPLETED'
                request_obj.save()
                elevator.current_floor = requested_floor
                elevator.is_open = True
                elevator.save()

    get_floor(elevator)
    serializer = RequestSerializer(request_obj)
    return Response(serializer.data, status=status.HTTP_201_CREATED)