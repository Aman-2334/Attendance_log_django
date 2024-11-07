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
        fields = ['id', 'name', 'email', 'password',
                  'registration', 'role', 'institute']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_role(self, value):
        print(f"user serializer validate role value: {value} {value.id}")
        if not Role.objects.filter(pk=value.id).exists():
            raise serializers.ValidationError("Role does not exist.")
        return value

    def validate_institute(self, value):
        print(f"user serializer validate institute value: {value} {value.id}")
        if not Institution.objects.filter(pk=value.id).exists():
            raise serializers.ValidationError("Institute does not exist.")
        return value

    def create(self, validated_data):
        print(f"serializer create called with data: {validated_data}")
        role = validated_data.pop('role', None)
        institute = validated_data.pop('institute', None)
        print(f"role {role}, institute: {institute}")
        if role is None:
            raise serializers.ValidationError(
                {"role": "This field is required."})

        if institute is None:
            raise serializers.ValidationError(
                {"institute": "This field is required."})

        user = User(**validated_data)
        user.set_password(validated_data['password'])
        # user.save()

        # User_Role.objects.create(user=user, role=role)

        # User_Institute.objects.create(user=user, institute=institute)

        return user

    def to_representation(self, instance):
        print(f"user serializer to_representaion initial instance {instance}")
        user_role = User_Role.objects.filter(user=instance['id'])
        print(f"user serializer to_representaion user_role {user_role}")
        # user_institute = User_Institute.objects.filter(user=instance)
        # print(
        #     f"user serializer to_representaion user_institute {user_institute}")
        # instance['role'] = [r.role for r in user_role]
        # instance['institute'] = [i.institute for i in user_institute]
        instance['role'] = 3
        instance['institute'] = 16
        print(f"user serializer to_representaion final instance {instance}")
        representation = super().to_representation(instance)
        return representation
