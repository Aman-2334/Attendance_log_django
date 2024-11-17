from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from institution.models import Institution
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from institution.serializers import InstitutionSerializer, AdminSerializer, TeacherSerializer, StudentSerializer
from rest_framework import status

from authentication.models import Role
from constants import ErrorMessage

class InstitutionView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_institution(self, request, format=None):
        try:
            institute = Institution.objects.all()
            print("institute: ", institute)
            serializer = InstitutionSerializer(institute, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)  
        except Exception as e:
            print("Get Institution exception caught: ", e)
            return Response(ErrorMessage.get_error_response(),status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def filter_user_by_role(role, id, Serializer):
    try:
        User = get_user_model()
        role = Role.objects.get(role = role)
        users = User.objects.filter(role_id = role.pk, institute_id = id)
        serializer = Serializer(users,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        raise e

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_institution_admin(request, id):
    try:
        return filter_user_by_role(role='ADMIN', id=id, Serializer=AdminSerializer)
    except Exception as e:
        print("Get Institution Admin exception caught: ",e)
        return Response(ErrorMessage.get_error_response(),status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])  
def get_institution_teacher(request, id):
    try:
        return filter_user_by_role(role='TEACHER', id=id, Serializer=TeacherSerializer)
    except Exception as e:
        print("Get Institution Teacher exception caught: ",e)
        return Response(ErrorMessage.get_error_response(),status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])   
def get_institution_student(request, id):
    try:
        return filter_user_by_role(role='STUDENT', id=id, Serializer=StudentSerializer)
    except Exception as e:
        print("Get Institution Student exception caught: ",e)
        return Response(ErrorMessage.get_error_response(),status=status.HTTP_500_INTERNAL_SERVER_ERROR)