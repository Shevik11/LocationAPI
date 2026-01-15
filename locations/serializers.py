from .models import Locations
from rest_framework import serializers


class LocationsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    average_rating = serializers.FloatField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    feedback_count = serializers.SerializerMethodField()

    class Meta:
        model = Locations
        fields = ["id", "name", "category", "average_rating", "created_at", "updated_at", "feedback_count"]

    def get_feedback_count(self, obj):
        return obj.feedbacks.count()
