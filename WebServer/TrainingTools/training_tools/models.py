from django.db import models

class Image(models.Model):
    image           = models.ImageField(upload_to='uploads')

class FaceImage(models.Model):
    original_image  = models.ForeignKey(Image) 
    image           = models.ImageField(upload_to='uploads')

class Person(models.Model):
    faces = models.ManyToManyField(FaceImage)

class Group(models.Model):
    people  =   models.ManyToManyField(Person)
    images  =   models.ManyToManyField(Image)
    faces   =   models.ManyToManyField(FaceImage)    

# Create your models here.
