from django.db import models
from django.urls import reverse

import datetime

# Create your models here.
class Url(models.Model):
    original_url            = models.CharField(max_length=500)
    hashed_url              = models.CharField(max_length=50)
    clicks                  = models.PositiveIntegerField(default=0)
    creator_IP              = models.CharField(max_length=15, default="none")
    expires_after           = models.DateField(
        default=datetime.datetime.now() + datetime.timedelta(days=7)
    )
    expires_after_x_clicks  = models.PositiveIntegerField(default=0)

class History(models.Model):
    url             = models.ForeignKey(Url, on_delete=models.CASCADE)
    ip_address      = models.GenericIPAddressField()
    date_time       = models.DateTimeField(auto_now_add=True)
