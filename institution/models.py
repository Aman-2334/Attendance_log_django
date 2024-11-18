from django.db import models
from django.conf import settings


class Institution(models.Model):
    name = models.CharField(max_length=512)

    def __str__(self) -> str:
        return self.name


class Subject(models.Model):
    subject_name = models.CharField(max_length=512)
    subject_code = models.CharField(max_length=512)
    institution = models.ForeignKey(
        Institution, on_delete=models.CASCADE, related_name="subject_in_institution")
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="subject_instructor")
    student = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="student_in_subject")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['subject_code', 'institution'],
                name='unique_subject_in_institution'
            )
        ]

    def __str__(self):
        return f"{self.code},{self.name},{self.insititution}"
