from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import F

from ipware.ip import get_client_ip

from .forms import UrlCreateForm
from .forms import UrlEditForm
from .models import Url
from .models import UrlHistory

import random
import string
import datetime

# Create your views here.
def create_short_url_view(request):
    form = UrlCreateForm(request.POST or None)

    short_url = None  # Declare short_url variable

    current_IP, is_routable = get_client_ip(request)

    if form.is_valid():

        # Create random string of 10 ascii letters
        id_url = "".join(random.choice(string.ascii_letters) for x in range(10))

        # Check if it already exists
        while Url.objects.filter(new_url=id_url) == None:
            id_url = "".join(random.choice(string.ascii_letters) for x in range(10))

        # Set model variables
        form.instance.new_url = id_url
        form.instance.creator_IP = current_IP

        short_url = request.build_absolute_uri() + "r/" + id_url

        form.save()
        form = UrlCreateForm()

    context = {
        "form": form,
        "short_url": short_url,
    }

    return render(request, "urlshortener.html", context)


def redirect_view(request, url_id):
    site = Url.objects.get(new_url=url_id)

    # Increment clicks
    site.clicks = F("clicks") + 1
    site.save()

    # Creating another instance because if i used site.clicks again it was read as "CombinedExpression"
    my_instance = Url.objects.get(new_url=url_id)

    # Check if it's outdated
    if my_instance.expires_after < datetime.date.today():
        my_instance.delete()
        UrlHistory.objects.filter(url_id=url_id).delete()
        return HttpResponse("<h1>Link out of date</h1")

    # Check if it has reached the clicks threshold
    if (
        my_instance.expires_after_x_clicks != 0
        and my_instance.clicks > my_instance.expires_after_x_clicks
    ):
        my_instance.delete()
        UrlHistory.objects.filter(url_id=url_id).delete()
        return HttpResponse("<h1>Reached maximum number of redirects threshold</h1")

    # Get IP address
    current_IP, is_routable = get_client_ip(request)

    # Add a "history" entry
    UrlHistory.objects.create(url_id=url_id, ip_address=current_IP)

    return redirect(site.original_url)


def list_urls_view(request):
    current_IP, is_routable = get_client_ip(request)

    # List of all links created by a user (IP)
    created_links = Url.objects.filter(creator_IP=current_IP)

    site_url = request.build_absolute_uri() + "r/"

    context = {"created_links": created_links, "site_url": site_url}

    return render(request, "list_urls.html", context)


def delete_url_view(request, url_id):
    link = Url.objects.get(new_url=url_id)
    UrlHistory.objects.filter(url_id=url_id).delete()
    link.delete()
    return redirect("../")


def edit_url_view(request, url_id):
    url_to_edit = Url.objects.get(new_url=url_id)
    form = UrlEditForm(request.POST or None, instance=url_to_edit)

    if form.is_valid():
        form.save()
        form = UrlEditForm(request.POST or None, instance=url_to_edit)

    context = {"form": form}

    return render(request, "edit_url.html", context)


def history_url_view(request, url_id):
    current_url_history = UrlHistory.objects.filter(url_id=url_id)

    context = {"current_url_history": current_url_history}

    return render(request, "history_url.html", context)
