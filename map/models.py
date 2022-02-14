from django.db import models
from brand.models import Brand
from user.models import User
from datetime import datetime, timedelta
from django.utils import timezone
from multiselectfield import MultiSelectField
from django.core.validators import MaxValueValidator, MinValueValidator
 # Create your models here.

# 부스 이름, 부스 종류, 부스 주소, 부스 운영시간, 부스 브랜드
class Booth(models.Model):
    name = models.CharField(max_length=100)
    location = models.TextField()
    #operationHour = models.TimeField()
    operationHour = models.CharField(max_length=50)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    user = models.ManyToManyField(User, through='Liked', through_fields=('booth', 'user'))
    # 좌표
    x = models.CharField(max_length=50)
    y = models.CharField(max_length=50)

    ## 리뷰로 받는 것들
    street = models.IntegerField(default=0) # 길거리인지(0), 매장인지(1)
    deco = models.CharField(max_length=50) # 소품 (없 0 있 1)
    iron = models.IntegerField(default=0) # 고데기 (없 0 있 1)
    boxnum = models.IntegerField(default=0) # 부스 갯수 (갯수마다)

    rating = models.FloatField(default=0) # 별점, 기본값은 0, 별점은 0.5 부터 0.5 단위로?
    likenum = models.IntegerField(default=0) # 이 매장의 좋아요
    review_number = models.IntegerField(default=0)

    def __str__(self):
        return self.name + "("+str(self.brand)+")"

# user - liked - booth 다 대 다 연결
class Liked(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #user = models.OneToOneField(User, on_delete=models.SET_DEFAULT, default=None)
    dolike = models.BooleanField(default = False)
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE)
    date = models.DateField()

# 리뷰 작성할 부스, 리뷰 작성하는 user, title, 리뷰 작성한 시간, 사진, 별점
# tag 추가해야

class Review(models.Model):

    TAG_CHOICES = (
        ('시설이 깨끗해요','시설이 깨끗해요'),
        ('소품이 다양해요','소품이 다양해요'),
        ('부스가 많아요','부스가 많아요'),
        ('고데기가 있어요','고데기가 있어요'),
        ('로드점이에요','로드점이에요'),
    )
    COLOR_CHOICES = (
        ('핑크','핑크'),
        ('하늘','하늘'),
        ('노랑','노랑'),
        ('회색','회색'),
        ('남색','남색'),
        ('연두','연두'),
        ('보라', '보라'),
        ('빨강', '빨강'),
        ('주황', '주황'),

   )

    booth = models.ForeignKey(Booth, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now, blank=True)
    boothid = models.IntegerField(default=0)
    rate = models.IntegerField(default=0,
                               validators=[
                                   MaxValueValidator(5),
                                   MinValueValidator(0),
                               ]
                               )
    title = MultiSelectField(choices = TAG_CHOICES)
    color = MultiSelectField(choices = COLOR_CHOICES)



