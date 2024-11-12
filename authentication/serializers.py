from rest_framework import serializers
from django.contrib.auth import get_user_model
from authentication.models import Role
from institution.models import Institution


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'role']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'

    def create(self, validated_data):
        User = get_user_model()
        user = User(
            email=validated_data['email'],
            name=validated_data['name'],
            role=validated_data['role'],
            registration=validated_data['registration'],
            institute=validated_data['institute'],
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user
