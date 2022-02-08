from django.db import models
from map.models import Booth
from user.models import User

# Create your models here.

TAG_CHOICE = (
    (0, '분실'),
    (1, '보관'),
    (2, '기타')
)

class LnF_Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE)
    
    title = models.CharField(max_length=100)
    content = models.TextField()
    tag = models.IntegerField(default=0, choices=TAG_CHOICE)



class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(LnF_Post, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    content = models.TextField()


