from django.db import models

# Create your models here.

# o/x -> 0, 1로 해서 구분하면 될듯
# 브랜드명, 재쵤영 여부, 리모컨, 가격, qr 여부
class Brand(models.Model):
    name = models.CharField(max_length=50, unique= True)
    retake = models.IntegerField()
    remote = models.IntegerField()
    QR = models.IntegerField()
    etc = models.TextField(null=True)

    def __str__(self):
        return self.name



class Frame(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    name = models.CharField(max_length=50)
    # 4cut, 6cut 등
    frame = models.CharField(max_length=50)
    # 촬영take 수
    take = models.IntegerField()
    # 2장 기준
    price = models.IntegerField()
    # 촬영 시간
    time = models.CharField(max_length=50)

    def __str__(self):
        return self.name

