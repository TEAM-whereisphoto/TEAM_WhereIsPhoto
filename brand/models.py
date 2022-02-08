from django.db import models

# Create your models here.

# o/x -> 0, 1로 해서 구분하면 될듯
# 브랜드명, 재쵤영 여부, 촬영시간, 리모컨, 가격, qr 여부
class Brand(models.Model):
    name = models.CharField(max_length=50)
    retake = models.IntegerField()
    time = models.CharField(max_length=50)
    remote = models.IntegerField()
    price = models.TextField()
    QR = models.IntegerField()

    def __str__(self):
        return self.name