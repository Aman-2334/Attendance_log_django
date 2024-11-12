from django.shortcuts import render
from rest_framework.views import APIView
from institution.models import Institution
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from institution.serializers import InstitutionSerializer
from rest_framework import status


class InstitutionView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request, format=None):
        institute = Institution.objects.all()
        print("institute: ", institute)
        serializer = InstitutionSerializer(institute, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
