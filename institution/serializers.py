from rest_framework import serializers

from .models import Institution

class InstitutionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=512)