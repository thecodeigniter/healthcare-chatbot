from ast import keyword
from typing import final

from datetime import datetime
from .models import *
from chatbot.utils import *
import json
from webproject.settings import QUERIES_PATH
from django.db.models import Q

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

def nearest_hospital(request):
    latitude = request.session.get("latitude", False)
    longitude = request.session.get("longitude", False)
    
    if (latitude == False or longitude == False):
        return "Sorry I cannot tell. You have not provided us your current location information."
    
    try:
        info = Hospital.objects.all().values("id", "name", "gps_location", "address", "contact")
        displacement = []
        for i in range(len(info)):
            displacement.append(distance((float(latitude), float(longitude)), gps_coordinates(info[i]["gps_location"])))
        index = displacement.index(min(displacement))
        request.session["current_hospital"] = info[index]
        return "The closest hospital to you is "+info[index]["name"]+" located at "+info[index]["address"]+". Their contact number is: "+info[index]["contact"]
    except:
        return "Some error occured while fetching results. Please clear your cookies and try again"    

def no_of_departments(request):
    hospital = request.session.get("current_hospital", False)
    if (hospital == False):
        return "You have not asked about any hospital yet."
    else:
        no_of_departments = Department.objects.filter(hospital_id = hospital["id"]).count()
    
    if (no_of_departments == 0):
        return "Sorry I have no information regarding number of departments in "+hospital["name"]+"."
    elif (no_of_departments == 1):
        return "There is only one department in "+hospital["name"]+"."
    return "There are "+str(no_of_departments)+" departments in "+hospital["name"]+"."

def name_of_departments(request):
    hospital = request.session.get("current_hospital", False)
    if (hospital == False):
        return "You have not asked about any hospital yet."
    else:
        departments = Department.objects.filter(hospital_id = hospital["id"]).values("name")
        if (len(departments) == 0):
            return "Sorry! I have no information about departments in "+hospital["name"]+"."
        final_string = "The list is given below:\n"
        for i in range(len(departments)):
            final_string += str(i+1)+": "+departments[i]["name"]+"\n"
        return final_string


def hospital_location(request):
    keyword = request.session.get("current_keyword", False)
    if (keyword == False):
        return "Sorry We don't have information about it."
    hospital = Hospital.objects.filter(name__contains=keyword)
    if (len(hospital) == 0):
        return "Sorry! We don't have information about this hospital."
    request.session["current_hospital"] = hospital[0].name
    return hospital[0].name+\
            " located at "+hospital[0].address+\
                ". Their contact number is: "+hospital[0].contact

def doctor_in_department(request):
    keyword = request.session.get("current_keyword", False)
    hospital_name = request.session.get("current_hospital", False)
    if (keyword == False and hospital_name == False):
        return "Sorry We don't have information about it."
    

    try:
        hospital = Hospital.objects.get(name = hospital_name)
        department = Department.objects.get(hospital_id = hospital.id,
                                            name = keyword)
        doctors_detail = DoctorDetail.objects.filter(department_id = department.id, 
                                                )
    except:
        return "No results are found. Make sure to ask the question again from start."
    
    final_str = "Yes! following doctors are present in "+keyword+" department:\n"
    for i in range(len(doctors_detail)):
        final_str += str(i+1)+": "+str(doctors_detail[i].doctor.person)+" | "+doctors_detail[i].doctor.qualification+"\n"
    return final_str

def appointment_with_doctor(request):
    keyword = request.session.get("current_keyword", False)
    if (keyword == False):
        return "Sorry We don't have information about it."
    doctor = get_doctor_profile(keyword)
    if (doctor == None):
        return "Sorry! We don't have information about this doctor"
    
    detail = DoctorDetail.objects.get(doctor_id = doctor.id)
    if (detail.on_leave):
        return "Sorry, your requested doctor is on the leave"
    return "You can contact Dr. "+doctor.person.user.first_name+" "+ \
        doctor.person.user.last_name+" from " + \
        str(detail.availability_start)+" to "+str(detail.availability_end)+". " \
            +"Contact details are: "+doctor.person.contact

    
    
    
    
    
    