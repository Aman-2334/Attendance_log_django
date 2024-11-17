from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"(?P<institition_id>\d+)/subject", views.SubjectViewSet, basename='Subject')

urlpatterns = [
    path("", views.InstitutionView.as_view()),
    path("<int:id>/admin", views.get_institution_admin),
    path("<int:id>/teacher", views.get_institution_teacher),
    path("<int:id>/student", views.get_institution_student),
]
