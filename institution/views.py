from django.shortcuts import render
from rest_framework.views import APIView
from institution.models import Institution
from rest_framework.response import Response
from institution.serializers import InstitutionSerializer

class InstitutionView(APIView):
    def get(self, request, format=None):
        institute = Institution.objects.all()
        serializer = InstitutionSerializer(institute)
        return Response(serializer)