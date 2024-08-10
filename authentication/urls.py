from django.urls import path
from . import views

urlpatterns = [
    path('validate', views.Access_token_validation.as_view()),
    path('user/create', views.SignUp.as_view()),
]
