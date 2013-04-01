from django.db import models

class Actor(models.Model):
    name=models.CharField(max_length=256) # Name
    imdb=models.CharField(max_length=256) # #Imdb page
    notes=models.CharField(max_length=512) # Notes
    def __unicode__(self):
        return self.name

class Classifier(models.Model):
    actor = models.ForeignKey(Actor)
    fischer_faces=models.FileField(upload_to='classifiers/fischer')
    eigen_faces=models.FileField(upload_to='classifiers/eigen')
    LBP_faces=models.FileField(upload_to='classifiers/lbp')
    operator=models.CharField(max_length=256) # Name of operator who inputed this
    notes=models.CharField(max_length=256) # Notes
    
# Create your models here.
