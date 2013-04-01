from django.db import models

# Create your models here.
class Actor
    name            =   models.CharField(max_length=200)
    imdb_profile    =   models.CharField(max_length=200)
    notes           =   models.CharField(max_length=200)
    def __unicode__(self):
        return self.name

class Pictures
    image_file      =   models.ImageFile()
    
    
