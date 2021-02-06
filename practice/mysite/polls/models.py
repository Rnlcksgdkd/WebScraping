
from django.db import models

# Create your models here.
    
class Host_info(models.Model):
    host_name = models.CharField(max_length = 50)
    host_href = models.CharField(max_length = 100)
    host_rating = models.IntegerField(default = 0)
    host_num_rating = models.IntegerField(default = 0)
    host_region = models.CharField(max_length = 50)

    def __str__(self):
        return self.host_name

# 
class Accomodation(models.Model):
    roomID = models.TextField()
    rome_name = models.TextField()
    location = models.TextField()
    latitude = models.TextField()
    longitude = models.TextField()
    link = models.URLField()
    image_link = models.URLField()

