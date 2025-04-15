from .models import Locations
from rest_framework import serializers


class LocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = ["name", "category"]
