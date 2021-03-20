from django.contrib import admin
from .models import Url
from .models import UrlHistory

# Register your models here.
admin.site.register(Url)
admin.site.register(UrlHistory)
