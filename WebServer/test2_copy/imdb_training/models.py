from django.db import models

# Create your models here.
class Actor(models.Model):
    name            =   models.CharField(max_length=200)
    imdb_profile    =   models.CharField(max_length=200)
    notes           =   models.CharField(max_length=200)
    def __unicode__(self):
        return self.name

class Classifier(models.Model):
    actor           =   models.ForeignKey(Actor)
    Fischer         =   models.FileField(upload_to='classifiers/fischer')     
    def __unicode__(self):
        return self.actor.name;
