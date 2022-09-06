from django.db import models
from django.contrib.auth.models import User


class Card(models.Model):
    patient = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    diagnosis = models.CharField(max_length=250)
    condition = models.TextField(help_text="Patient's condition during treatment")
    recommendations = models.TextField(help_text="Recommendations and medications")
    is_recovered = models.BooleanField()


