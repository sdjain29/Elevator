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
            elevator = Elevator.objects.create()
            elevators.append(elevator)

        serializer = ElevatorSerializer(elevators, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)