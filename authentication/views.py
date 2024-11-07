from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status

from .serializers import UserSerializer
from .models import User
# Create your views here.


class Access_token_validation(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        content = {"message": "valid access token"}
        return Response(content, content_type='application/json')


class SignUpView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        print("Signup post request")
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            print("signup serializer is valid")
            serializer.create(validated_data=serializer.validated_data)
            print("signup serializer.create succesful")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, id):
        try:
            user = User.objects.filter(pk=id)
            user.delete()
            return Response({"detail": "User deleted Successfully!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"details": e}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
