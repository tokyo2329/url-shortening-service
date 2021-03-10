from django.db import models
import datetime

# Create your models here.
class Url(models.Model):
	original_url			= models.URLField()
	new_url					= models.CharField(max_length=10)
	clicks					= models.PositiveIntegerField(default=0)
	creator_IP				= models.CharField(max_length=15, default='none')
	expires_after			= models.DateField(default=datetime.datetime.now() + datetime.timedelta(days=7))
	expires_after_x_clicks	= models.PositiveIntegerField(default=0)

class UrlHistory(models.Model):
	url_id		= models.CharField(max_length=10)
	ip_address	= models.GenericIPAddressField()
	date_time	= models.DateTimeField(auto_now_add=True)