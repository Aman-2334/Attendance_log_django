from django.urls import path
from . import views

urlpatterns = [
    path("", views.InstitutionView.as_view()),
    path("<int:id>/admin", views.get_institution_admin),
    path("<int:id>/teacher", views.get_institution_teacher),
    path("<int:id>/student", views.get_institution_student),
]
