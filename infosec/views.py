from pyexpat import model
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from infosec.utils import exist_in_tuple, clip, get_proper_noun, generate
from webproject.settings import BASE_DIR, infosec_app, OPENAI_API_KEY, OPENAI_ENGINE, MAX_COOKIE_LIFE
import os
import openai
from random import random
import numpy as np
from django.contrib.auth.models import User
#from .models import Configuration, Disease, Person, Query
#from chatbot.text_to_speech import NaturalTTS
openai.api_key = OPENAI_API_KEY
import json


# Create your views here.
def index(request):
    user = request.session.get("user_info", False)
    
    
    if (user == False):
        return redirect('/')
    
    u = User.objects.get(email = user)
        
    content = {
        
                "company_name":"Infosec by Transdata Inc.",
                "company_website":"https://transdata.biz/gateway/",
                "message": "Enjoy your chatbot!",
                "user_name":u.first_name+" "+u.last_name,
            }
    return render(request,infosec_app+"chat.html", content)



def send_response(request):
    user = request.session.get("user_info", False)  
    if (user == False):
        return JsonResponse({
            "output":"You have not provided credentials."
            })
    message = request.POST.get("message")
    
    #keyword = get_proper_noun(message)
    #request.session["current_keyword"] = keyword
    #rule_response = select_function(message, keyword)
    
   
    message_to_api = "You: "+message+"\nInfoSecBot: "
    
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
    
   
    
    # audio_file = str(1)+"_audio_"+generate(random_chars = 10)
    # for mp3_file in os.listdir("static"):
    #     result = mp3_file.split(str(1)+"_audio_")[0]
    #     if result == "":
    #         os.remove(os.path.join(BASE_DIR, "static", mp3_file))
    # NaturalTTS(content["output"], audio_file)
    #content["voice"] = audio_file+".mp3"
    #content["voice"] = None
    
            
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
    

    
        