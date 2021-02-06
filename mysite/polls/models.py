
from django.db import models

# Create your models here.
    
# models.py 추가
class Accomodation(models.Model):
    roomID = models.TextField()
    room_name = models.TextField()
    location = models.TextField()
    latitude = models.TextField()
    longitude = models.TextField()
    link = models.URLField()
    image_link = models.URLField()

    def __str__(self):
        return self.room_name

    def update(self, list):
        self.roomID = list[0]
        self.room_name = list[1]
        self.location = list[2]
        self.latitude = list[3]
        self.longitude = list[4]
        self.link = list[5]
        self.image_link = list[6]