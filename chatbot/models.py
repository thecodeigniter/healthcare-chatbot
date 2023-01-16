
from django.db import models
from django.forms import IntegerField
from django_countries.fields import CountryField
from django.contrib.auth.models import User
from .constants import (GENDERS, ROOMS, CURRENCY, RATE, TYPE_OF_QUERY, TYPE_OF_WARDS, TYPE_OF_EMBEDDINGS)
from django.core.exceptions import ValidationError
#from django.contrib.postgres.fields import ArrayField

# Create your models here.

class common(models.Model):
    country = CountryField()
    state = models.CharField(max_length=15)
    city = models.CharField(max_length=15)
    contact = models.CharField(max_length=20)
    address = models.CharField(max_length=300, blank = True)
    gps_location = models.CharField(max_length=50, blank=True)
    
    class Meta:
        abstract = True

    
class Person(common):
    
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    ssn = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDERS)
    
    def __str__(self):
        return self.user.first_name+" "+self.user.last_name+" ("+self.user.email+")"

class Hospital(common):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Department(models.Model):
    hospital = models.ForeignKey('Hospital', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name+" | "+self.hospital.name
    
    
class Doctor(models.Model):
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    qualification = models.CharField(max_length=100)
    experience = models.IntegerField()
    speciality = models.CharField(max_length=40)
    is_surgeon = models.BooleanField()
    
    def __str__(self):
        return self.person.user.first_name+" "+self.person.user.last_name+" | "+self.qualification
    

class DoctorDetail(models.Model):
    doctor = models.OneToOneField('Doctor', on_delete=models.CASCADE) 
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    availability_start = models.TimeField()
    availability_end = models.TimeField()
    on_leave = models.BooleanField(default=False)
    
class Disease(models.Model):
    person = models.OneToOneField('Person', on_delete=models.CASCADE)
    symptoms = models.TextField(blank = True)
    history = models.TextField(blank= True)
    precautions = models.TextField(blank = True)
    
    def __str__(self):
        return self.person.user.first_name+" "+self.person.user.last_name+" details"

class Room(models.Model):
    hospital = models.ForeignKey('Hospital', on_delete=models.CASCADE)
    room_number = models.IntegerField()
    _type = models.CharField(max_length=6, choices=ROOMS)
    fare = models.IntegerField()
    fare_currency = models.CharField(max_length=3, choices=CURRENCY)
    charging_rate = models.CharField(max_length=4, choices=RATE)
    
class Ward(models.Model):
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    _type = models.CharField(max_length=3, choices=TYPE_OF_WARDS)
    ventilator = models.IntegerField()
    bed = models.IntegerField()
    
class Configuration(models.Model):
    def save(self, *args, **kwargs):
        if not self.pk and Configuration.objects.exists():
            raise ValidationError('There is can be only one JuicerBaseSettings instance')
        return super(Configuration, self).save(*args, **kwargs)

    threshold = models.FloatField()

class Query(models.Model):
    function = models.CharField(max_length=100)
    question = models.CharField(max_length=300)
    engine = models.CharField(max_length=10, choices=TYPE_OF_EMBEDDINGS, default="ada")
    embeddings = models.TextField()
    type_of_question = models.CharField(max_length=10, choices=TYPE_OF_QUERY, default = "simple")
    
    def __str__(self):
        return self.function

    
    
    
    