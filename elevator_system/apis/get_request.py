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
            return Response({'error': 'Elevator in Maintenance.'}, status=status.HTTP_404_NOT_FOUND)

        requests = elevator.requests.filter(status='PENDING')
        serializer = RequestSerializer(requests, many=True)

        return Response(serializer.data)

    # Explanation: API endpoint for fetching all pending requests for a given elevator.
    # It retrieves the elevator based on the provided elevator_id.
    # If the elevator does not exist or is in maintenance mode, an appropriate error response is returned.
    # It filters the requests for the elevator with 'PENDING' status.
    # Then, it serializes the pending requests using the RequestSerializer.
    # Finally, it returns the serialized data as the response.
