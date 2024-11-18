from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Institution, Subject

class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = '__all__'

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id','email','name']

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id','email','name']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id','email','name']

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        exclude=['student']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        User = get_user_model()
        data['instructor'] = TeacherSerializer(User.objects.get(pk = data['instructor'])).data
        return data
    