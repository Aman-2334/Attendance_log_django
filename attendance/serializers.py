from rest_framework import serializers

class OnlineAttendanceSerializer(serializers.Serializer):
    imageUrls = serializers.ListField(
        child = serializers.CharField(max_length=1000)
    )