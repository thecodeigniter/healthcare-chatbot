from django.http import HttpResponse
from django.shortcuts import render, redirect
from passlib.hash import pbkdf2_sha256 as sha256
import random
from django.contrib.auth.models import User
from webproject import settings
from django.contrib.auth.hashers import check_password

def generate(random_chars=24, alphabet="0123456789abcdefghijklmnopqrstABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    r = random.SystemRandom()
    return ''.join([r.choice(alphabet) for i in range(random_chars)])


def login(request):

    user = request.session.get("user_info", False)
    if (user == False):
        
        if (request.method == "GET"):
        
            
            content = {
                'submit_data':"",
                'notification':"",
            }
            return render(request, 'login.html', content)
        elif(request.method == "POST"):
            
            try:
                u = User.objects.get(username  = request.POST.get("username"))
                if (check_password(request.POST.get("password"), u.password)):
                    content = {
                    "company_name":"Transdata Inc.",
                    "company_website":"https://transdata.biz/gateway/",
                    "message": "Welcome "+u.first_name+" "+u.last_name+" to Transdata AI Applications Testing"
                    }
                    response = render(request, "welcome.html", content)
                    if (request.POST.get("remember") == "on"):
                        request.session["user_info"] = u.email
                    return response
                else:
                    content = {
                        'submit_data':"",
                        'notification':"Wrong username or password. Please try again",
                        }

                return render(request, 'login.html', content)
                    
            except:
                content = {
                'submit_data':"",
                'notification':"Wrong username or password. Please try again",
                }

                return render(request, 'login.html', content)
        else:
            return HttpResponse("Bad method")
    else:
        u = User.objects.get(email = user)
        content = {
                    "company_name":"Transdata Inc.",
                    "company_website":"https://transdata.biz/gateway/",
                    "message": "Welcome "+u.first_name+" "+u.last_name+" to Transdata AI Applications Testing"
                    }
        return render(request, "welcome.html", content)
    
        
def logout(request):
    user = request.session.get("user_info", False)  
    response = redirect('/')
    if (user != False):
        try:
            
            request.session["user_info"] = False
        except:
            return HttpResponse("Wrong cookie given")
        
    return response
    
    