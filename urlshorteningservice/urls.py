"""urlshorteningservice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from urlshortener.views import (
    CreateShortUrl,
    UrlRedirect,
    ListUrls,
    UrlDelete
    )
from urlshortener.views import edit_url_view
from urlshortener.views import history_url_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", CreateShortUrl.as_view(success_url="/"), name="home"),
    path("r/<str:hashed_url>", UrlRedirect.as_view(), name="redirect"),
    path("list-urls/", ListUrls.as_view(), name="list"),
    path("list-urls/<pk>/delete", UrlDelete.as_view(), name="delete"),
    path("list-urls/<str:url_id>/edit", edit_url_view, name="edit"),
    path("list-urls/<str:url_id>/history", history_url_view, name="history"),
]
