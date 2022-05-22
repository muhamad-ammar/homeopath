from django.db import models

class Profile(models.Model):
    content = models.TextField()

class userDocData(models.Model):
    userCID = models.CharField(max_length=200)
    userDID = models.CharField(max_length=100)
    userName = models.CharField(max_length=100)
   
class patientData(models.Model):
    patientID = models.CharField(max_length=100, unique=True)
    userDID = models.CharField(max_length=100)
    patientName = models.CharField(max_length=100)
    patientDate = models.CharField(max_length=100)
    remedies = models.CharField(max_length=500)
    age = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    feedback=models.BooleanField(default=0)
    
class updated_weights(models.Model):
    userDID = models.CharField(max_length=100)
    patientID = models.CharField(max_length=100)
    rubricRemedies = models.CharField(max_length=200)
    age = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    weight=models.IntegerField()

class remidieAndRuubricsRecord(models.Model):
    rubric = models.CharField(max_length=200)
    remidieID = models.CharField(max_length=100)
    rubricID = models.CharField(max_length=100)
    remedy = models.CharField(max_length=100)
    rating = models.CharField(max_length=100)
    timesUsed = models.IntegerField()