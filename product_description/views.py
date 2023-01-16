
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from webproject.settings import product_description_app, OPENAI_API_KEY
import os
import openai
from django.contrib.auth.models import User
openai.api_key = OPENAI_API_KEY
from random import random
# Create your views here.
def index(request):
    user = request.session.get("user_info", False)  
    if (user == False):
        return redirect('/')
    content = {
                    "company_name":"Transdata Inc.",
                    "company_website":"https://transdata.biz/gateway/",
                    "message": "Production Description Generator is coming soon. Please be patient. Thanks! "
                    }
    return render(request,  product_description_app+"selection.html", content)

def generate(request):
      
    user = request.session.get("user_info", False)  
    if (user == False):
        return JsonResponse({
            "user_history":"",
            "output":"You have not provided credentials."
            })
    
    content = {}
    
    try:
        upper = request.POST.get("upper")
        lining = request.POST.get("lining")
        sole = request.POST.get("sole")
        fastening = request.POST.get("fastening")
        trim = request.POST.get("trims")
        leg = request.POST.get("leg")
        insole = request.POST.get("insole")
        
        text = "Create a creative and amazing product description for a shoe with "
        
        if (insole == "true"):
            text = text+"removeable insoles, "
        
        text = text+upper+" upper material, "
        text = text+lining+" lining material, "
        text = text+sole+" sole, "
        text = text+fastening+" fastening type, "
        text = text+trim+" trims, and "
        text = text+leg+" boot leg height: \n"
        
        result = get_response(text)
        
        

        content = {
            "message": result["choices"][0]["text"],
            "status": True
        }
    
    except:
        content = {
            "message": "Not uploaded",
            "status": False,
        }
    
    return JsonResponse(content)

def get_response(sequence):
    response = openai.Completion.create(engine="text-davinci-002",
    prompt=sequence,
    temperature=0.5+random()*0.5,
    max_tokens=100,
    top_p=0.3+random()*0.5,
    frequency_penalty=0.5+random()*0.5,
    presence_penalty=0+random()*0.5)
    
    return response