from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import F
from django.views.generic import (
    CreateView,
    RedirectView,
    ListView,
    DeleteView
    )

from ipware.ip import get_client_ip
from hashids import Hashids

from .forms import UrlCreateForm
from .forms import UrlEditForm
from .models import Url
from .models import UrlHistory

import random
import string
import datetime


class CreateShortUrl(CreateView):
    model = Url
    fields = ['original_url']

    def form_valid(self, form):

        # Setting the IP
        current_IP, is_routable = get_client_ip(self.request)
        form.instance.creator_IP = current_IP

        # Hashing the url
        hashids = Hashids()
        form.instance.hashed_url = hashids.encode(id(form.instance))
        form.save()

        #created_url = self.request.build_absolute_uri() + "r/" + form.instance.hashed_url
        return redirect("home")
    #self.request.build_absolute_uri() + "r/" + form.instance.hashed_url   

class UrlRedirect(RedirectView):

    permanent = False
    query_string = True
    pattern_name = 'redirect'

    def get_redirect_url(self, *args, **kwargs):
        url = get_object_or_404(Url, hashed_url=kwargs['hashed_url'])
        return convert_text_to_url(url.original_url)

class ListUrls(ListView):

    context_object_name = 'urls'

    def get_queryset(self):
        current_IP, is_routable = get_client_ip(self.request)
        print(Url.objects.filter(creator_IP=current_IP))
        return Url.objects.filter(creator_IP=current_IP)

class UrlDelete(DeleteView):
    model = Url
    success_url = "../"
    

def edit_url_view(request, url_id):
    url_to_edit = Url.objects.get(hashed_url=url_id)
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

def convert_text_to_url(text):

    if text.find("www.") == -1:
        text = "www." + text

    if text.find("http://") == -1 and text.find("https://") == -1:
        text = "http://" + text

    return text