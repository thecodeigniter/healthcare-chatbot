"""webproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import login, logout
from django.conf import settings
from django.conf.urls.static import static
from webproject.settings import chatbot_app, product_description_app, infosec_app

admin.site.site_header = "Transdata Healthbot Admin"
admin.site.site_title = "Transdata Healthbot Admin Portal"
admin.site.index_title = "Welcome to Transdata Healthbot"


urlpatterns = [
    path('admin/', admin.site.urls),
    path(chatbot_app, include('chatbot.urls')),
    path(product_description_app, include('product_description.urls')),  
    path(infosec_app, include('infosec.urls')),  
    path('', login, name = 'login'),
    path('logout/', logout, name = 'logout'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
