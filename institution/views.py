from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from institution.models import Institution, Subject
from institution.serializers import InstitutionSerializer, AdminSerializer, TeacherSerializer, StudentSerializer, SubjectSerializer
from authentication.models import Role
from helper import ErrorMessage

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
        return filter_user_by_role(role='INSTITUTION ADMIN', id=id, Serializer=AdminSerializer)
    except Exception as e:
        print("Get Institution Admin exception caught: ",e)
        return Response(ErrorMessage().get_error_response(),status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])  
def get_institution_teacher(request, id):
    try:
        return filter_user_by_role(role='INSTRUCTOR', id=id, Serializer=TeacherSerializer)
    except Exception as e:
        print("Get Institution Teacher exception caught: ",e)
        return Response(ErrorMessage().get_error_response(),status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])   
def get_institution_student(request, id):
    try:
        return filter_user_by_role(role='STUDENT', id=id, Serializer=StudentSerializer)
    except Exception as e:
        print("Get Institution Student exception caught: ",e)
        return Response(ErrorMessage().get_error_response(),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class SubjectViewSet(ModelViewSet):
    serializer_class = SubjectSerializer
    def get_queryset(self):
        institution_id = self.kwargs.get('institution_id') 
        return Subject.objects.filter(institution_id = institution_id)
    
    def checkIntegrityError(self, e):
        if isinstance(e.detail, dict) and "non_field_errors" in e.detail:
            for error in e.detail["non_field_errors"]:
                if "unique" in str(error).lower():
                    return Response(
                        {"detail": "A subject with this code already exists for this institution."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
        return None

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            print("Subject view set create exception: ",e)
            integrity_error = self.checkIntegrityError(e)
            if integrity_error:
                return integrity_error 
            return Response(ErrorMessage("An Error occured").get_error_response(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            print("Subject view set create exception: ",e)
            integrity_error = self.checkIntegrityError(e)
            if integrity_error:
                return integrity_error 
            return Response(ErrorMessage("An Error occured").get_error_response(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)