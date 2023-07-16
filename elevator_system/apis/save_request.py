from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Elevator, Request
from ..serializers import RequestSerializer
from django.db import transaction

class SaveUserInternalRequestView(APIView):
    def post(self, request, elevator_id):
        try:
            elevator = Elevator.objects.get(id=elevator_id)
        except Elevator.DoesNotExist:
            return Response({'error': 'Elevator does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        if elevator.is_operational == False:
            return Response({'error': 'Elevator in Maintainance.'}, status=status.HTTP_404_NOT_FOUND)

        requested_floor = request.data.get('floor')

        requests = elevator.requests.filter(status='PENDING', floor=requested_floor)
        if len(requests) != 0:
            serializer = RequestSerializer(requests)
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

        serializer = RequestSerializer(request_obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)