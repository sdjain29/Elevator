from django.urls import path
from .apis.initialize import ElevatorInitializationView
from .apis.save_request import SaveUserInternalRequestView, SaveUserExternalRequestView
from .apis.direction import CurrentDirectionView, NextDestinationView, SetElevatorDoorView
from .apis.elevator_status import SetElevatorOperationalView
from .apis.get_request import ElevatorRequestsView


urlpatterns = [
    path('api/elevator/initialize/', ElevatorInitializationView.as_view(), name='initialize_elevator'),
    # Explanation: API endpoint for initializing the elevator system by creating 'n' elevators.

    path('api/elevator/<int:elevator_id>/requests/', ElevatorRequestsView.as_view(), name='elevator_requests'),
    # Explanation: API endpoint for fetching all requests for a given elevator.

    path('api/elevator/<int:elevator_id>/next_destination/', NextDestinationView.as_view(), name='next_destination'),
    # Explanation: API endpoint for fetching the next destination floor for a given elevator.

    path('api/elevator/<int:elevator_id>/current_direction/', CurrentDirectionView.as_view(), name='current_direction'),
    # Explanation: API endpoint for fetching whether the elevator is currently moving up or down.

    path('api/elevator/<int:elevator_id>/save_request/', SaveUserInternalRequestView.as_view(), name='save_request'),
    # Explanation: API endpoint for saving a user's internal request (inside the elevator) to the list of requests for a specific elevator.

    path('api/elevator/<int:elevator_id>/door_action/', SetElevatorDoorView.as_view(), name='save_request'),
    # Explanation: API endpoint for opening and closing the elevator door.

    path('api/elevator/call/', SaveUserExternalRequestView.as_view(), name='call_elevator'),
    # Explanation: API endpoint for saving a user's external request (outside the elevator) to the list of requests for the most optimal elevator.

    path('api/elevator/<int:elevator_id>/set_operational/', SetElevatorOperationalView.as_view(), name='set_operational'),
    # Explanation: API endpoint for setting the operational status of an elevator.
]

