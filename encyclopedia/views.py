from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from markdown import markdown
from django import forms

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if entry := util.get_entry(title):
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": markdown(entry)
        })
    else:
        return render(request, "encyclopedia/404.html", status = 404)

def search(request):
    title = request.GET['q']
    if util.get_entry(title):
        return HttpResponseRedirect(reverse("entry", args=[title]))
    else:
        return render(request, "encyclopedia/search.html", {
            "entries": [entry for entry in util.list_entries() if title in entry]
        })
