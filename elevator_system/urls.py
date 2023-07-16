from django.urls import path
from .apis.initialize import ElevatorInitializationView
from .apis.save_request import SaveUserInternalRequestView, SaveUserExternalRequestView
from .apis.direction import CurrentDirectionView, NextDestinationView
from .apis.elevator_status import SetElevatorOperationalView
from .apis.get_request import ElevatorRequestsView


urlpatterns = [
    path('api/elevator/initialize/', ElevatorInitializationView.as_view(), name='initialize_elevator'),
    path('api/elevator/<int:elevator_id>/requests/', ElevatorRequestsView.as_view(), name='elevator_requests'),
    path('api/elevator/<int:elevator_id>/next_destination/', NextDestinationView.as_view(), name='next_destination'),
    path('api/elevator/<int:elevator_id>/current_direction/', CurrentDirectionView.as_view(), name='current_direction'),
    path('api/elevator/<int:elevator_id>/save_request/', SaveUserInternalRequestView.as_view(), name='save_request'),
    path('api/elevator/call_elevator', SaveUserExternalRequestView.as_view(), name='call_elevator'),
    path('api/elevator/<uuid:elevator_id>/set_operational/', SetElevatorOperationalView.as_view(), name='set_operational'),
]
