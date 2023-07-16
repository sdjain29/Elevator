from rest_framework import serializers
from .models import Elevator, Request

# Explanation: Serializer class for the Both model.
# It defines the fields to be included in the serialized representation of a Both object.
# In this case, it includes all the fields defined in the Both model.


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'

class ElevatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Elevator
        fields = '__all__'