from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Table(models.Model):
     user = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
     title=models.CharField(max_length=100,default="no title",blank=False)
     desc = models.CharField(max_length=255, default="no desc", blank=False)
     Datetime = models.DateTimeField()

     def __str__(self) -> str:
          return self.title