
from django.contrib import admin
from django.urls import path
from chatbot import views

urlpatterns = [
    path("", views.index, name = 'index'),
    path("send_response", views.send_response, name='Send Response'),
    path("set_location", views.set_location, name = "Set Location"),
    path("details", views.details, name = "Details"),
    path("get/embeddings", views.get_embeddings, name = "Get Embeddings"),
    path("set_query", views.set_query, name = "Set Query")
    
]