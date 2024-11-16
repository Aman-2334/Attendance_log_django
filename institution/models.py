from django.db import models

class Institution(models.Model):
    name = models.CharField(max_length=512)

    def __str__(self) -> str:
        return self.name