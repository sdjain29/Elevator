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
            return Response({'error': 'Elevator in Maintainance.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'current_direction': elevator.current_direction})

def get_floor(elevator):
    requests = elevator.requests.filter(status='PENDING')
    if not requests:
        elevator.current_direction = "IDLE"
        elevator.save()
        return

    current_floor = elevator.current_floor
    current_direction = elevator.current_direction

    if current_direction == "UP":
        next_destination = requests.filter(floor__gt=current_floor).order_by('floor').first()
        if next_destination:
            return next_destination
        else:
            next_destination = requests.filter(floor__lt=current_floor).order_by('-floor').first()
            if next_destination:
                elevator.current_direction = "DOWN"
                elevator.save()
                return next_destination
    else:
        next_destination = requests.filter(floor__lt=current_floor+1).order_by('-floor').first()
        if next_destination:
            return next_destination
        else:
            next_destination = requests.filter(floor__gt=current_floor).order_by('floor').first()
            if next_destination:
                elevator.current_direction = "UP"
                elevator.save()
                return next_destination

    return


class NextDestinationView(APIView):
    def get(self, request, elevator_id):
        try:
            elevator = Elevator.objects.get(id=elevator_id)
        except Elevator.DoesNotExist:
            return Response({'error': 'Elevator does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        if elevator.is_operational == False:
            return Response({'error': 'Elevator in Maintainance.'}, status=status.HTTP_404_NOT_FOUND)

        next_destination = get_floor(elevator)
        if next_destination == None:
            return Response({'next_destination': elevator.current_floor})

        return Response({'next_destination': next_destination.floor})
    

class SetElevatorDoorView(APIView):
    def post(self, request, elevator_id):
        try:
            elevator = Elevator.objects.get(id=elevator_id)
        except Elevator.DoesNotExist:
            return Response({'error': 'Elevator does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        if elevator.is_operational == False:
            return Response({'error': 'Elevator in Maintainance.'}, status=status.HTTP_404_NOT_FOUND)

        action = request.data.get('action')
        if action == 'open':
            elevator.is_open = True
            elevator.save()
            return Response({'status': 'Success'}, status=status.HTTP_200_OK)
        elif action == 'close':
            next_destination = get_floor(elevator)
            if next_destination ==  None:
                elevator.is_open = False
                elevator.save()
            else:
                with transaction.atomic():
                    next_destination.status = 'COMPLETED'
                    next_destination.save()
                    elevator.current_floor = next_destination.floor
                    elevator.is_open = True
                    elevator.save()
            return Response({'status': 'Success'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)