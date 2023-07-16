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

        # Update the is_operational flag of the elevator
        elevator.is_operational = is_operational
        elevator.save()
        
        # Cancel all pending requests for the elevator
        request_objs = elevator.requests.filter(status='PENDING')
        for i in request_objs:
            i.status = 'CANCELLED'
            i.save()

        return Response({'status': 'Success'}, status=status.HTTP_200_OK)

    # Explanation: API endpoint for setting the operational status of an elevator.
    # It retrieves the elevator based on the provided elevator_id.
    # If the elevator does not exist, an appropriate error response is returned.
    # It updates the is_operational flag of the elevator based on the provided value.
    # It also cancels all pending requests for the elevator by updating their status to 'CANCELLED'.
    # Finally, it returns a success response indicating the status has been updated successfully.

