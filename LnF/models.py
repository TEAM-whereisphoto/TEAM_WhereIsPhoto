from django.db import models
from map.models import Booth
from user.models import User
from datetime import datetime, timedelta
from django.utils import timezone


# Create your models here.

TAG_CHOICE = (
    ('분실', '분실'),
    ('보관', '보관'),
    ('기타', '기타')
)

class LnF_Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE)
    
    title = models.CharField(max_length=100)
    img = models.ImageField(blank=True, null=True, upload_to="LnF")
    content = models.TextField()
    tag = models.CharField(max_length=100, choices=TAG_CHOICE)
    time = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.title
    
    @property
    def timeString(self):
        now = timezone.now() - self.time
        if now < timedelta(minutes=1):
            return '방금 전'
        elif now < timedelta(hours=1):
            return str(int(now.seconds / 60)) + '분 전'
        elif now < timedelta(days=1):
            return str(int(now.seconds / 3600)) + '시간 전'
        elif now < timedelta(days=7):
            now = timezone.now().date() - self.time.date()
            return str(now.days) + '일 전'
        else:
            return False




class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(LnF_Post, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    
    content = models.TextField()
    time = models.DateTimeField(default=datetime.now, blank=True)
    
    read = models.IntegerField(default=0)

    @property
    def timeString(self):
        now = timezone.now() - self.time
        if now < timedelta(minutes=1):
            return '방금 전'
        elif now < timedelta(hours=1):
            return str(int(now.seconds / 60)) + '분 전'
        elif now < timedelta(days=1):
            return str(int(now.seconds / 3600)) + '시간 전'
        elif now < timedelta(days=7):
            now = timezone.now().date() - self.time.date()
            return str(now.days) + '일 전'
        else:
            return False


