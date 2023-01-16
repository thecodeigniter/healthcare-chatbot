from ast import keyword
from django.test import TestCase
from .models import *
from django.db.models import Q

keyword = "Dr. Ahmad Khalid"

def get_doctor_profile(keyword):
    
    keyword = keyword.replace("dr", "")
    keyword = keyword.replace(".", "")
    keyword = keyword.lstrip(" ")
    keyword = keyword.rstrip(" ")
    list_ = keyword.split(" ")
    q_object = Q(person__user__first_name__icontains=list[0]) | \
        Q(person__user__last_name__icontains=list[0])

    for item in list_[1:]:
        q_object.add((Q(person__user__first_name__icontains=item) | \
            Q(person__user__last_name__icontains=item)), q_object.connector)
    queryset = Doctor.objects.filter(q_object)
    if (len(queryset) == 0):
        return None
    return queryset[0]

print(get_doctor_profile("Dr. Ahmad Khalid"))
# Create your tests here.
