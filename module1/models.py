from django.db import models

class Profile(models.Model):
    content = models.TextField()
    
class patientData(models.Model):
    patientID = models.CharField(max_length=100, unique=True)
    remidies = models.CharField(max_length=500)
    rebrics = models.CharField(max_length=100)