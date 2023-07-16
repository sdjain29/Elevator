from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Elevator
from ..serializers import RequestSerializer
from django.db import transaction

class ElevatorRequestsView(APIView):
    def get(self, request, elevator_id):
        try:
            elevator = Elevator.objects.get(id=elevator_id)
        except Elevator.DoesNotExist:
            return Response({'error': 'Elevator does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        if elevator.is_operational == False:
            return Response({'error': 'Elevator in Maintainance.'}, status=status.HTTP_404_NOT_FOUND)

        requests = elevator.requests.filter(status='PENDING')
        serializer = RequestSerializer(requests, many=True)
        return Response(serializer.data)
