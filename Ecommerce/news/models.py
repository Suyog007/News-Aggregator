from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length= 200)
   
    def __str__(self):
        return self.name



class News(models.Model):
    id = models.AutoField(primary_key = True)
    news_title = models.CharField(max_length = 200)
    news_content = models.CharField(max_length = 2000)
    news_image = models.CharField(max_length = 200)
    source = models.CharField(max_length = 200, default = None)
    category = models.ForeignKey( 'Category' ,default = None, on_delete=models.DO_NOTHING)


    def __str__(self):
        return self.news_title


class Comments(models.Model):
    id = models.AutoField(primary_key = True)
    comment_content = models.CharField(max_length= 1000)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
