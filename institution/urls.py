from django.urls import path
from .views import InstitutionView

urlpatterns = [
    path("",InstitutionView.as_view()),
]
