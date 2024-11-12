from django.urls import path
from . import views

urlpatterns = [
    path('validate', views.Access_token_validation.as_view()),
    path('user', views.UserView.as_view()),
    path('user/<int:id>', views.UserView.as_view()),
]
