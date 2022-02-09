from hashlib import blake2b
from tkinter import CASCADE
from django.db import models
from brand.models import Brand
from user.models import User


# Create your models here.

# 부스 이름, 부스 종류, 부스 주소, 부스 운영시간, 부스 브랜드
class Booth(models.Model):
    name = models.CharField(max_length=100)
    location = models.TextField()
    #operationHour = models.TimeField()
    operationHour = models.CharField(max_length=50)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    user = models.ManyToManyField(User, through='Liked', through_fields=('booth', 'user'))
    rate = models.FloatField(default= 0, null=True)
    img = models.ImageField(blank=True, null=True, upload_to="")
    #user = models.OneToOneField(User, through='Liked', through_fields=('booth', 'user'), on_delete=models.SET_DEFAULT, default=None)


    def __str__(self):
        return self.name + "("+str(self.brand)+")"

# user - liked - booth 다 대 다 연결
class Liked(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #user = models.OneToOneField(User, on_delete=models.SET_DEFAULT, default=None)

    booth = models.ForeignKey(Booth, on_delete=models.CASCADE)
    date = models.DateField()


# 리뷰 작성할 부스, 리뷰 작성하는 user, title, 리뷰 작성한 시간, 사진, 별점
# tag 추가해야 됨
class Review(models.Model):
    IRON_CHOICES = (('YES', 'yes'), ('No', 'no'))
    STREET_CHOICES = (('STORE', 'store'), ('ROAD', 'road'))
    DECO_CHOICES = (('GLASS', 'glass'), ('BAND', 'band'), ('HAT', 'hat'))
    BOXNUM_CHOICES = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),('5_more', '5_more'))

    booth = models.ForeignKey(Booth, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #user = models.OneToOneField(User, on_delete=models.SET_DEFAULT, default=None)
    #title = models.CharField(max_length=100)
    date = models.DateField()
    img = models.ImageField(blank=True, null=True, upload_to="")
    rate = models.IntegerField()
    iron = models.CharField(choices=IRON_CHOICES, max_length=50)
    street = models.CharField(choices=STREET_CHOICES, max_length=50)
    deco = models.CharField(choices=DECO_CHOICES, max_length=50)
    boxnum = models.CharField(choices=BOXNUM_CHOICES, max_length=50)

    new = models.BooleanField(default=False)

