from rest_framework import serializers

from .models import Role

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'role']


class UserSerializer(serializers.ModelSerializer):
    pass