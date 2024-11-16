from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from institution.models import Institution
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from institution.serializers import InstitutionSerializer, AdminSerializer, TeacherSerializer, StudentSerializer
from rest_framework import status

from authentication.models import Role
from constants import ErrorMessage

class InstitutionView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request, format=None):
        institute = Institution.objects.all()
        print("institute: ", institute)
        serializer = InstitutionSerializer(institute, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def getInstitutionAdmin(request):
    try:
        User = get_user_model()
        role = Role.objects.get(role = 'ADMIN')
        admins = User.objects.filter(role = role.pk)
        serializer = AdminSerializer(admins,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        print("Get Institution Admin exception caught: ",e)
        return Response(ErrorMessage.get_error_response(),status=status.HTTP_500_INTERNAL_SERVER_ERROR) 