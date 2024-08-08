from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Role
from .enums import RoleChoice

class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 255)
    email = serializers.EmailField()
    password = serializers.CharField(max_length = 255)
    role = serializers.CharField(max_length = 255)

    def create(self, validated_data):
        try:
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
            )

            Role.objects.create(
                user = user,
                role = RoleChoice(validated_data['role']).name
            )
        except Exception as e:
            raise serializers.ValidationError(f"Error creating user: {str(e)}")
        

            

            