from django.urls import path
from django.urls import path, register_converter
from django.urls.converters import UUIDConverter
from .views import (
    ElevatorInitializationView,
    ElevatorRequestsView,
    NextDestinationView,
    CurrentDirectionView,
    SaveUserRequestView,
)

register_converter(UUIDConverter, 'uuid')

urlpatterns = [
    path('api/elevator/initialize/', ElevatorInitializationView.as_view(), name='initialize_elevator'),
    path('api/elevator/<int:elevator_id>/requests/', ElevatorRequestsView.as_view(), name='elevator_requests'),
    path('api/elevator/<int:elevator_id>/next_destination/', NextDestinationView.as_view(), name='next_destination'),
    path('api/elevator/<int:elevator_id>/current_direction/', CurrentDirectionView.as_view(), name='current_direction'),
    path('api/elevator/<int:elevator_id>/save_request/', SaveUserRequestView.as_view(), name='save_request'),
]
