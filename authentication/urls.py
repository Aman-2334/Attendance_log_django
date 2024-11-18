from django.urls import path
from . import views

urlpatterns = [
    path('validate/', views.Access_token_validation.as_view()),
    path('user/', views.User_View.as_view()),
    path('user/<int:id>/', views.User_View.as_view()),
    path('login/', views.signin_view.as_view(), name="login"),
]
