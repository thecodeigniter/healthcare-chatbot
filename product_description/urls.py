
from django.contrib import admin
from django.urls import path
from product_description import views

urlpatterns = [
    path("", views.index, name = 'index'),
    path("generate", views.generate, name = "generate")
]