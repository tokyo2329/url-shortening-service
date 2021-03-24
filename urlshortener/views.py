from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import F
from django.views.generic import (
    CreateView,
    RedirectView,
    ListView,
    DeleteView,
    UpdateView
    )

from ipware.ip import get_client_ip
from hashids import Hashids

from .models import Url
from .models import History

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

        # Check if it's outdated
        if datetime.date.today() > url.expires_after:
            url.delete()
            return "../"
        # Check if it's reached the max clicks threshold
        elif url.clicks > url.expires_after_x_clicks and url.expires_after_x_clicks != 0:
            url.delete()
            return "../"
        else:
            # Add a history entry
            current_IP, is_routable = get_client_ip(self.request)
            History.objects.create(url=url, ip_address=current_IP)

            # Increment clicks
            url.clicks = History.objects.filter(url=url).count()
            url.save()

            return convert_text_to_url(url.original_url)


class ListUrls(ListView):

    context_object_name = 'urls'
    paginate_by = 10

    def get_queryset(self):
        current_IP, is_routable = get_client_ip(self.request)
        return Url.objects.filter(creator_IP=current_IP)


class UrlDelete(DeleteView):
    model = Url
    success_url = "../"


class UrlEdit(UpdateView):
    model = Url
    fields = ["expires_after", "expires_after_x_clicks"]
    template_name_suffix = '_edit_form'
    success_url = "../"


class ListUrlHistory(ListView):

    context_object_name = 'ips'
    paginate_by = 10

    def get_queryset(self):
        return History.objects.filter(url=self.kwargs['pk'])


def convert_text_to_url(text):

    if text.find("www.") == -1:
        text = "www." + text

    if text.find("http://") == -1 and text.find("https://") == -1:
        text = "http://" + text

    return text