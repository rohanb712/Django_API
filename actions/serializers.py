from rest_framework import serializers
from datetime import datetime

class ActionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    action = serializers.CharField(max_length=255, required=True)
    date = serializers.DateField(required=True)
    points = serializers.IntegerField(required=True)
    
    def validate_action(self, value):
        if not value.strip():
            raise serializers.ValidationError("Action cannot be empty.")
        return value.strip()
    
    def validate_points(self, value):
        if value < 0:
            raise serializers.ValidationError("Points must be a positive integer.")
        return value
    
    def validate_date(self, value):
        if value > datetime.now().date():
            raise serializers.ValidationError("Date cannot be in the future.")
        return value