from django.shortcuts import render
from django import forms
import random as rand
import markdown2

from . import util

class EntryForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Title','class':'input-group'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Place your markdown content here.','class':'input-group'}))
    
def index(request):

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def entry(request, title):
    
    entry = util.get_entry(title)
    
    return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": markdown2.markdown(entry)
        })
        
    
def search(request):
    # check if have post request
    if request.method == "POST":
        searchText = request.POST.get('q')
        
        entry = util.get_entry(searchText)
    
        # go to entry page if found entry
        if entry:
            return render(request, "encyclopedia/entry.html", {
                "title": searchText,
                "entry": markdown2.markdown(entry)
            })
        # display search page if searching text not match
        else:
            return render(request, "encyclopedia/search.html",{
                "entries": util.list_entries(),
                "searchText": searchText
            })

def add(request):
    
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            
            newEntry = {
                "title" : form.cleaned_data['title'],
                "content": form.cleaned_data['content']
            }
            
            # check if title already exists
            existingEntry = util.get_entry(newEntry.get("title"))
            
            # if title is existing, then return error message
            if existingEntry:
                return render(request,"encyclopedia/add.html",{
                    "form": form,
                    "errorMessage": "Title '{}' already exists.".format(newEntry.get('title'))
                })
                
            # if title is not existing, then create new entry and render new entry page
            util.save_entry(newEntry.get('title'), newEntry.get('content'))
            
            return render(request, "encyclopedia/entry.html", {
                "title": newEntry.get('title'),
                "entry": markdown2.markdown(newEntry.get('content'))
            })
        else:
            return render(request,"encyclopedia/add.html",{
                "form": form
            })
            
    return render(request, "encyclopedia/add.html",{
        "form": EntryForm()
    })
    
def edit(request, title):
    # if title is not provided, then return to entry page
    
    # get current entry and pass it to form
    entry = util.get_entry(title)
        
    # create edit form
    form = EntryForm(initial={"title":title,"content": entry})
    
    return render(request, "encyclopedia/edit.html",{
        "form": form
    })
    
def update(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            
            newEntry = {
                "title" : form.cleaned_data['title'],
                "content": form.cleaned_data['content']
            }
                
            # if title is not existing, then create new entry and render new entry page
            util.save_entry(newEntry.get('title'), newEntry.get('content'))
            
            return render(request, "encyclopedia/entry.html", {
                "title": newEntry.get('title'),
                "entry": markdown2.markdown(newEntry.get('content'))
            })
        else:
            # return to edit form if data not valid
            return render(request,"encyclopedia/edit.html",{
                "form": form
            })
    
    # return to index page if do not have post request
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def random(request):
    # get entry list
    entries = util.list_entries()
    
    # random title
    title = entries[rand.randint(0, len(entries)-1)]
    
    # get entry by title
    entry = util.get_entry(title)
    
    # display entry page
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": markdown2.markdown(entry)
    })

    
    
    