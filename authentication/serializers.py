from rest_framework import serializers

from .models import Role, User, User_Role, User_Institute
from institution.models import Institution


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'role']


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Role
        fields = ['user', 'role']


class UserInstituteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Institute
        fields = ['user', 'institute']


class UserSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())
    institute = serializers.PrimaryKeyRelatedField(
        queryset=Institution.objects.all())

    class Meta:
        model = User
        fields = ['name', 'email', 'password',
                  'registration', 'role', 'institute']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_role(self, value):
        if not Role.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Role does not exist.")
        return value

    def validate_institute(self, value):
        if not Institution.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Institute does not exist.")
        return value

    def create(self, validated_data):
        role = validated_data.pop('role')
        institute = validated_data.pop('institute')

        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        User_Role.objects.create(user=user, role=role)

        User_Institute.objects.create(user=user, institute=institute)

        return user
