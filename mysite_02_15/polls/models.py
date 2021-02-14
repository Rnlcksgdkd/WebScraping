from django.contrib.auth.models import User
from django.db import models

# Create your models here.
    
# models.py 추가
class Accomodation(models.Model):
    roomID = models.TextField()
    room_name = models.TextField()
    city = models.TextField(null=True , blank = True)
    location = models.TextField()
    latitude = models.TextField()
    longitude = models.TextField()
    accomodation_type = models.TextField(null=True , blank = True)
    min_price = models.IntegerField(null=True , blank = True)
    rating = models.FloatField(null=True , blank = True)
    general_review = models.TextField(null=True , blank = True)
    total_review_num = models.IntegerField(null=True , blank = True)
    owner_comment = models.TextField(null =True , blank=True)
    image_link = models.URLField(null=True)
    img_link_2 = models.URLField(null=True , blank = True)
    img_link_3 = models.URLField(null=True , blank = True)
    img_link_4 = models.URLField(null=True , blank = True)
    img_link_5 = models.URLField(null=True , blank = True)
    
    def __str__(self):
        return self.room_name

    def update(self, list):
        self.roomID = list[0]
        self.room_name = list[1]
        self.city = list[2]
        self.location = list[3]
        self.latitude = list[4]
        self.longitude = list[5]
        self.accomodation_type = list[6]
        if list[7] != " "  and list[7] != None:  self.min_price = list[7]
        if list[8] != " "  and list[8] != None: self.rating = list[8]
        if list[9] != " "  and list[9] != None: self.general_review = list[9]
        if list[10] != " " and list[10] != None: self.total_review_num = int(list[10])
        if list[11] != " " : self.owner_comment = list[11]
        self.image_link = list[12]
        self.img_link_2 = list[13]
        self.img_link_3 = list[14]
        self.img_link_4 = list[15]
        self.img_link_5 = list[16]
       # if list[16] != " ": self.owner_comment = list[16]


# 방에 대한 데이터 테이블
class Room_detail(models.Model):
    
    room_id = models.ForeignKey('Accomodation', on_delete=models.CASCADE, db_column='roomID')
    room_types = models.TextField(null=True , blank = True)
    room_prices = models.IntegerField(null=True , blank = True)
    room_img = models.URLField(null=True , blank = True)

    def __str__(self):
        if self.room_types == None : return ("전체 매진")
        elif self.room_prices == None : return ("매진")
        else:  return self.room_types

    def update(self , list):
        self.room_id = Accomodation.objects.all().filter(roomID = list[0])[0]
        if list[1] != " " : self.room_types = list[1]
        if list[2] != " " : self.room_prices = list[2]
        if list[3] != " " : self.room_img = list[3]


#게시판 데이터
class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)  #계정이 삭제되면 계정과 연결된 Question 모델 데이터를 모두 삭제하라
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()

    def __str__(self):
        return self.subject

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
