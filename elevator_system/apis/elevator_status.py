from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Elevator, Request
from ..serializers import ElevatorSerializer, RequestSerializer
from django.db import transaction


class SetElevatorOperationalView(APIView):
    def post(self, request, elevator_id):
        try:
            elevator = Elevator.objects.get(id=elevator_id)
        except Elevator.DoesNotExist:
            return Response({'error': 'Elevator does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        is_operational = request.data.get('is_operational')

        elevator.is_operational = is_operational
        elevator.save()
        
        request_objs = elevator.requests.filter(status='PENDING')
        for i in request_objs:
            i.status = 'CANCELLED'
            i.save()

        return Response({'status': 'Success'}, status=status.HTTP_200_OK)
    



