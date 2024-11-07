from django.urls import path
from . import views

urlpatterns = [
    path('validate', views.Access_token_validation.as_view()),
    path('user/create', views.SignUpView.as_view()),
    path('user/delete/<int:id>', views.DeleteView.as_view()),
]
