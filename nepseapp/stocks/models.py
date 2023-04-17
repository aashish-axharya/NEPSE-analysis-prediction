from django.db import models
from django.contrib.auth.models import User

class StockData(models.Model):
    sn = models.CharField(max_length=10)
    symbol = models.CharField(max_length=10)
    company_name = models.CharField(max_length=100)
    conf = models.CharField(max_length=10)
    open = models.CharField(max_length=10)
    high =models.CharField(max_length=10)
    low = models.CharField(max_length=10)
    close =models.CharField(max_length=10)
    vwap = models.CharField(max_length=10)
    volume = models.CharField(max_length=10)
    prev_close = models.CharField(max_length=10)
    turnover = models.CharField(max_length=10)
    trans = models.CharField(max_length=10)
    diff = models.CharField(max_length=10)
    range = models.CharField(max_length=10)
    diff_percent = models.CharField(max_length=10)
    range_percent = models.CharField(max_length=10)
    vwap_percent = models.CharField(max_length=10)
    days120 = models.CharField(max_length=10)
    days180 = models.CharField(max_length=10)
    weeks52_high = models.CharField(max_length=10)
    weeks52_low = models.CharField(max_length=10)

    def get_favorited_by(self):
        favorites = Favorite.objects.filter(stock=self)
        return [favorite.user for favorite in favorites]


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(StockData, on_delete=models.CASCADE)