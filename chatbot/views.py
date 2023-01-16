from pyexpat import model
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from chatbot.utils import exist_in_tuple, clip, get_proper_noun, generate
from webproject.settings import BASE_DIR, chatbot_app, OPENAI_API_KEY, OPENAI_ENGINE, MAX_COOKIE_LIFE
import os
import openai
from random import random
import numpy as np
from chatbot.queries import *
from django.contrib.auth.models import User
from .constants import starting_prompt, TYPE_OF_EMBEDDINGS
from .models import Configuration, Disease, Person, Query
from chatbot.text_to_speech import NaturalTTS
openai.api_key = OPENAI_API_KEY
import json
from .queries import *


# Create your views here.
def index(request):
    user = request.session.get("user_info", False)
    
    
    if (user == False):
        return redirect('/')
    
    is_location_set = True
    if (request.session.get("longitude", False) == False 
        or 
        request.session.get("latitude", False) == False):
        is_location_set = False
    u = User.objects.get(email = user)
        
    content = {
        
                "company_name":"Transdata Inc.",
                "company_website":"https://transdata.biz/gateway/",
                "message": "Enjoy your chatbot!",
                "user_name":u.first_name+" "+u.last_name,
                "location_set":is_location_set,
                
            }
    return render(request,chatbot_app+"chat.html", content)

def details(request):
    user = request.session.get("user_info", False)

    if (user == False):
        return redirect('/')
    person_history = ""
    u = User.objects.get(email = user)
    try:
        
        person_history = Disease.objects.get(person_id = 
                                                   Person.objects.get(user = u).id).history
        
        sending_text = "Summarize the conversation:\n"+person_history+"\n\nSummary:"
        person_summary =  get_response(sending_text, 150, 1.0, 0.7, 0, "-davinci-002")["choices"][0]["text"]
        
        
    except:
        d = Disease(person_id = Person.objects.get(user = u).id,
                    history =person_history)
        d.save()
    
        
    content = {
        
                "company_name":"Transdata Inc.",
                "company_website":"https://transdata.biz/gateway/",
                "user_name":u.first_name+" "+u.last_name,
                "user_history":person_history,
                "user_summary":person_summary,   
            }
    return render(request,chatbot_app+"details.html",content)

def set_location(request):
    longitude = request.POST.get("longitude")
    latitude = request.POST.get("latitude")
    
    cookie_long = request.session.get("longitude", False)
    cookie_lat = request.session.get("latitude", False)
    
    message = ""
    if (cookie_long == False or cookie_lat == False):
        message = "Location has been set. Please refresh the page to get your coordinates"
    else:
        message = "Your coordinates are: "+str(round(float(cookie_long),4))+", "+str(round(float(cookie_lat),4))
        
        
    
    response = JsonResponse({
                            "message":message,
                            "status":True,
                            "longitude":cookie_long,
                            "latitude":cookie_lat
                             }
                            )
    request.session["longitude"]= longitude
    request.session["latitude"]= latitude
    return response

def send_response(request):
    user = request.session.get("user_info", False)  
    if (user == False):
        return JsonResponse({
            "output":"You have not provided credentials."
            })
    message = request.POST.get("message")
    keyword = get_proper_noun(message)
    request.session["current_keyword"] = keyword
    #rule_response = select_function(message, keyword)
    rule_response = None
   
    message_to_api = "You: "+message+"\nHealthbot: "
    if (rule_response != None):
        bot_response = eval(rule_response)(request)
        bot_response = bot_response.lstrip("\n")
        content = {"output":bot_response}
        bot_response = message_to_api+bot_response+"\n"
        
    else:    
        try:
            bot_response =  get_response(message_to_api, 100)["choices"][0]["text"]
            bot_response = bot_response.lstrip("\n")
            bot_response = message_to_api+bot_response.split(message_to_api)[-1]+"\n"    
            content = {
                "output":bot_response.split(message_to_api)[-1]
        }
        except:
            content = {
                "output":"Sorry, you have reached the free API limit use."
            }
    
    #d = Disease.objects.get(person_id =
    #                               Person.objects.get(user = User.objects.get(email = user)).id)
    #d.history = d.history+bot_response
    #d.save()
    
    # audio_file = str(1)+"_audio_"+generate(random_chars = 10)
    # for mp3_file in os.listdir("static"):
    #     result = mp3_file.split(str(1)+"_audio_")[0]
    #     if result == "":
    #         os.remove(os.path.join(BASE_DIR, "static", mp3_file))
    # NaturalTTS(content["output"], audio_file)
    #content["voice"] = audio_file+".mp3"
    content["voice"] = None
        
            
    return JsonResponse(content)
       
def get_response(sequence, no_of_tokens = 100,
                 top_p_value = 0.3,
                 temperature_value = 0.5,
                 frequency_penalty_value = 0.5,
                 engine_type = OPENAI_ENGINE):
    response = openai.Completion.create(engine="text"+engine_type,
    prompt=sequence,
    temperature=clip(temperature_value+random()*0.3),
    max_tokens=no_of_tokens,
    top_p=clip(top_p_value+random()*0.3),
    frequency_penalty=clip(frequency_penalty_value+random()*0.3),
    presence_penalty=clip(0+random()*0.2)
    )
    
    return response


def select_function(sentence, keyword):
    
    question_type = "simple"
    if (keyword != None):
        question_type = "keyword"
    response= openai.Embedding.create(input=sentence, engine="text-similarity"+OPENAI_ENGINE)
    embedding = np.array(response['data'][0]['embedding'])
    scores = []
    queries = Query.objects.filter(type_of_question =
                                   question_type).values("function", 
                                                    "embeddings", "engine")
    
    for query in queries:
            db_embedding = [float(i) for i in (query["embeddings"]).split(", ")]
            known_embedding = np.array(db_embedding)
            scores.append(1-round((np.linalg.norm(embedding-known_embedding)),4))
    max_score = max(scores)
    if (max_score > Configuration.objects.first().threshold):
        return queries[scores.index(max_score)]["function"]
    return None
    

def get_embeddings(request):
    response= openai.Embedding.create(input=request.POST.get("sentence"),
                                      engine="text-similarity"+OPENAI_ENGINE)
    return JsonResponse({
        "embeddings":response['data'][0]['embedding'],
    })
    
def set_query(request):
    function = request.POST.get("function")
    question = request.POST.get("question")
    engine = request.POST.get("engine")
    _type = request.POST.get("type")
    if (not exist_in_tuple(TYPE_OF_EMBEDDINGS, engine)):
        content = {
                "output":"Engine must be 'ada', 'davinci', 'babbage' or 'curie'"
            }
        return JsonResponse(content)
    
    if (not exist_in_tuple(TYPE_OF_QUERY, _type)):
        content = {
                "output":"Type must be 'simple' or 'keyword'"
            }
        return JsonResponse(content)
    response= openai.Embedding.create(input=question,
                                      engine="text-similarity"+OPENAI_ENGINE)
    
    embeddings = ", ".join(map(str, response['data'][0]['embedding']))
    
    try:
        q = Query(function = function,
                  question = question, 
                  engine = engine,
                  embeddings = embeddings,
                   type_of_question = _type)
        q.save()
        content = {
                "output":"Query has been added. Make sure you have inserted function as well."
            }
    except:
        content = {
            "output":"Failed"
        }
    
    return JsonResponse(content)
    
        