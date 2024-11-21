from django.contrib.auth import get_user_model, login
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.authentication import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from .serializers import UserSerializer
from .models import User
from helper import ErrorMessage


class Access_token_validation(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        content = {"message": "valid access token"}
        return Response(content, content_type='application/json')


class User_View(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_authenticators(self):
        if self.request.method == 'POST':
            return []
        return super().get_authenticators()

    def get_permissions(self):
        if self.request.method == 'POST':
            return []
        if self.request.method == "DELETE":
            return [IsAdminUser()]
        return super().get_permissions()

    def get(self, request, id):
        User = get_user_model()
        users = User.objects.get(pk=id)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                response_data = {
                    'user': serializer.data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return Response(response_data, status=status.HTTP_200_OK)
            except Exception as e:
                print(
                    "Exception Raised -> User Sign up request -> serializer.save() -> ", e)
                return Response({"details": "Error occured while creating user!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            user = User.objects.filter(pk=id)
            if user:
                user.delete()
                return Response({"details": "User deleted Successfully!"}, status=status.HTTP_200_OK)
            else:
                return Response(ErrorMessage("No such user found!").get_error_response(), status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print("Exception Raised -> User delete request -> ", e)
            return Response({"details": e}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

class signin_view(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            try:
                login(request=request, user=user)
                serializer = UserSerializer(user)
                refresh = RefreshToken.for_user(user)
                response_data = {
                    'user': serializer.data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return Response(response_data, status=status.HTTP_200_OK)
            except Exception as e:
                print("Exception Raised -> User login -> ", e)
                return Response({"details": "An Error Occured!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"details": "User not found!"}, status=status.HTTP_404_NOT_FOUND)
