from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Elevator
from ..serializers import ElevatorSerializer

class ElevatorInitializationView(APIView):
    def post(self, request):
        num_elevators = request.data.get('num_elevators')

        elevators = []
        for _ in range(num_elevators):
            # Create the specified number of elevators
            elevator = Elevator.objects.create()
            elevators.append(elevator)

        # Serialize the created elevators
        serializer = ElevatorSerializer(elevators, many=True)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Explanation: API endpoint for initializing the elevator system by creating a specified number of elevators.
    # It expects the number of elevators to be created in the request data.
    # It creates the specified number of elevators and stores them in a list.
    # Then, it serializes the created elevators using the ElevatorSerializer.
    # Finally, it returns the serialized data as the response with a status code of 201 (Created).
