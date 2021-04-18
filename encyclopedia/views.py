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

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Entry Title")
    entry = forms.CharField(label="Entry Text", widget=forms.Textarea)

def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html", {
            "form": NewEntryForm()
        })
    
    form = NewEntryForm(request.POST)
    if form.is_valid():
        title = form.cleaned_data["title"]
        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/400.html", status = 400)
        content = form.cleaned_data["entry"]
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry", args=[title]))
    else:
        return render(request, "encyclopedia/create.html", {
            "form": form
        })
    
class NewEditForm(forms.Form):
    entry = forms.CharField(label="Entry Text", widget=forms.Textarea)

def edit(request):
    title = request.POST['entry']
    entry = util.get_entry(title)
    if not entry:
        return render(request, "encyclopedia/404.html", status = 404)
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "form": NewEditForm(initial={"entry": entry})
    })


def save(request):
    form = NewEditForm(request.POST)
    if form.is_valid():
        title = request.POST['title']
        entry = form.cleaned_data["entry"]
        print(title, entry)
        util.save_entry(title, entry)
        return HttpResponseRedirect(reverse("entry", args=[title]))
