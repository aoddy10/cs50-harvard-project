from django.urls import path

from . import views

app_name = 'encyclopedia'
urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("add", views.add, name="add"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("update", views.update, name="update"),
    path("random", views.random, name="random"),
    path("<str:title>", views.entry, name="entry"),
]
