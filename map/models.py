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
    operationHour = models.CharField(max_length=50)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    user = models.ManyToManyField(User, through='Liked', through_fields=('booth', 'user'))

    ## 리뷰로 받는 것들
    street = models.IntegerField(default=0) # 길거리인지(0), 매장인지(1)
    deco = models.IntegerField(default=0) # 소품 (없 0 있 1)
    iron = models.IntegerField(default=0) # 고데기 (없 0 있 1)
    boxnum = models.IntegerField(default=0) # 부스 갯수 (갯수마다)

    rating = models.IntegerField(default=0) # 별점, 기본값은 0, 별점은 0.5 부터 0.5 단위로?
    likenum = models.IntegerField(default=0) # 이 매장의 좋아요 수

    def __str__(self):
        return self.name + "("+str(self.brand)+")"


# user - liked - booth 다 대 다 연결
class Liked(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE)
    date = models.DateField()


# 리뷰 작성할 부스, 리뷰 작성하는 user, title, 리뷰 작성한 시간, 사진, 별점
# tag 추가해야 됨
class Review(models.Model):
    # IRON_CHOICES = (('YES', 'yes'), ('No', 'no')),
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    date = models.DateField()
    img = models.ImageField(blank=True, null=True, upload_to="")
    rate = models.IntegerField()
    # iron = models.CharField(choices=IRON)