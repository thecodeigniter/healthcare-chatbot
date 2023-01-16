import numpy as np
import nltk 
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize, sent_tokenize
from webproject import settings
from django.core.mail import send_mail
from random import SystemRandom
nltk.download("averaged_perceptron_tagger")
nltk.download("punkt")
nltk.download("stopwords")


def generate(random_chars=24, alphabet="0123456789abcdefghijklmnopqrstABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    r = SystemRandom()
    return ''.join([r.choice(alphabet) for i in range(random_chars)])

class Mail:
    email_from = settings.EMAIL_HOST

    def __init__(self,message = None,recipient_list=None, subject="Healthbot by Transdata Inc."):
        try:
            print("---------------------trying for mail -----------------")
            send_mail(subject,message,self.email_from,recipient_list)
        except:
            return None

def get_proper_noun(text):
    string = ""
    sentences = nltk.sent_tokenize(text)
    for sentence in sentences:
        words = nltk.word_tokenize(sentence)
        words = [word for word in words if word not in set(stopwords.words('english'))]
        tagged = nltk.pos_tag(words)
        for (word, tag) in tagged:
            if tag == 'NNP': # If the word is a proper noun
                string += word+" "
    if (string == ""):
        return None
    return string[:-1]

def distance(point_1, point_2, is_meters = False):
    threshold = 100
    if (is_meters):
        threshold = threshold*1000
    return (np.linalg.norm(np.array(point_1) - np.array(point_2)))*threshold

def gps_coordinates(gps_str):
    return float(gps_str.split(", ")[0]), float(gps_str.split(", ")[1]) 

def exist_in_tuple(tuple, value):
    for pair in tuple:
        if (value in pair):
            return True
    return False

def clip(value):
    if (value <= 0.0):
        value = 0.0
    elif (value >= 1.0):
        value = 0.99
    else:
        pass
    return value