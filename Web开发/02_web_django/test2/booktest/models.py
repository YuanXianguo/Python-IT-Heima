from django.db import models


class BookInfo(models.Model):
    title = models.CharField(max_length=20)
    pub_date = models.DateField(auto_now_add=True)
    read = models.IntegerField(default=0)
    comment = models.IntegerField(default=0)
    is_delete = models.BooleanField(default=False)


class HeroInfo(models.Model):
    name = models.CharField(max_length=20)
    gender = models.BooleanField(default=False)
    comment = models.CharField(max_length=128)
    is_delete = models.BooleanField(default=False)
    book = models.ForeignKey('BookInfo', on_delete=models.CASCADE)
