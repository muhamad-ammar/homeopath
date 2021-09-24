from django.db import models

class Profile(models.Model):
    content = models.TextField()
    
class patientData(models.Model):
    patientID = models.CharField(max_length=100, unique=True)
    remedies = models.CharField(max_length=500)
    rubrics = models.CharField(max_length=100)
    feedback=models.BooleanField(default=0)