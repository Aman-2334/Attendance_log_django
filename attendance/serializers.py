from rest_framework import serializers
from .models import AttendanceSession, AttendanceImages
from institution.serializers import SubjectSerializer


class OnlineAttendanceSerializer(serializers.Serializer):
    imageUrls = serializers.ListField(
        child=serializers.CharField(max_length=1000)
    )


class AttendanceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceImages
        fields = ['id', 'image']


class AttendanceSessionSerializer(serializers.ModelSerializer):
    images = AttendanceImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(),
        required=False
    )

    class Meta:
        model = AttendanceSession
        fields = ['id', 'classCount', 'date', 'startTime',
                  'endTime', 'students', 'subject', 'images', 'uploaded_images']

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        attendance_session = AttendanceSession.objects.create(**validated_data)
        for image in uploaded_images:
            AttendanceImages.objects.create(
                attendance_session=attendance_session, image=image)
        return attendance_session
