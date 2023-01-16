
from django.contrib import admin
from django.urls import path
from infosec import views

urlpatterns = [
    path("", views.index, name = 'index'),
    path("send_response", views.send_response, name='Send Response'), 
]