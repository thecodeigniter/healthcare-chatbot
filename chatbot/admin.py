
from django.contrib import admin
from .models import (Person, Doctor, Hospital, 
                     Department, Disease, Room,
                     Ward, DoctorDetail, Configuration, Query)

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'hospital', 'name',)

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'person', 'qualification', 'experience', 'speciality', 'is_surgeon')

class DoctorDetailAdmin(admin.ModelAdmin):
    list_display= ('id', 'doctor', 'department', 'availability_start', 'availability_end', 'on_leave')

class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'hospital', 'room_number', '_type', 'fare', 'fare_currency', 'charging_rate')

class WardAdmin(admin.ModelAdmin):
    list_display = ('id', 'department', '_type', 'ventilator', 'bed')

class ConfigurationAdmin(admin.ModelAdmin):
    list_display= ('threshold',)

class QueryAdmin(admin.ModelAdmin):
    list_display = ('function', 'question', 'engine', 'type_of_question')




# Register your models here.

admin.site.register(Person)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Hospital)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Disease)
admin.site.register(Room, RoomAdmin)
admin.site.register(Ward, WardAdmin)
admin.site.register(DoctorDetail, DoctorDetailAdmin)
admin.site.register(Configuration, ConfigurationAdmin)
admin.site.register(Query, QueryAdmin)