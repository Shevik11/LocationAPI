from .models import Feedback
from rest_framework import serializers
from locations.models import Locations


class FeedbackSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    user = serializers.StringRelatedField(read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    location = serializers.StringRelatedField(read_only=True)
    location_id = serializers.IntegerField(write_only=True, required=True)
    location_name = serializers.CharField(source='location.name', read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Feedback
        fields = [
            "id",
            "user",
            "user_id",
            "location",
            "location_id",
            "location_name",
            "comments",
            "comments_like",
            "comments_dislike",
            "stars",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["user", "user_id", "created_at", "updated_at"]

    def validate_location_id(self, value):
        try:
            Locations.objects.get(id=value)
        except Locations.DoesNotExist:
            raise serializers.ValidationError("Location with this ID does not exist.")
        return value

    def validate_stars(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Stars must be between 1 and 5.")
        return value

    def create(self, validated_data):
        location_id = validated_data.pop('location_id', None)
        if location_id:
            location = Locations.objects.get(id=location_id)
            validated_data['location'] = location
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'location_id' in validated_data:
            location_id = validated_data.pop('location_id')
            location = Locations.objects.get(id=location_id)
            validated_data['location'] = location
        return super().update(instance, validated_data)
