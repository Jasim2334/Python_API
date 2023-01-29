# Create your models here.
from django.db import models

def image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<name>/<filename>
    return '{0}/{1}'.format(instance.name, filename)


class Address(models.Model):
    hno = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)

class WorkExperience(models.Model):
    companyName = models.CharField(max_length=255)
    fromDate = models.DateField()
    toDate = models.DateField()
    address = models.CharField(max_length=255)

class Qualification(models.Model):
    qualificationName = models.CharField(max_length=255)
    fromDate = models.DateField()
    toDate = models.DateField()
    percentage = models.FloatField()

class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()


class Person(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    age = models.IntegerField()
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    phoneNo = models.CharField(max_length=255, blank=True)
    addressDetails = models.ForeignKey(Address, on_delete=models.CASCADE)
    workExperience = models.ManyToManyField(WorkExperience)
    qualifications = models.ManyToManyField(Qualification)
    projects = models.ManyToManyField(Project)
    photo = models.ImageField(upload_to=image_directory_path,blank=True,null=True)
 
