from django.db import models

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


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)