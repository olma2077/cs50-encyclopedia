from django.shortcuts import render
from markdown import markdown
from django.http import Http404

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
