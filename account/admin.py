from django.contrib import admin
from .models import *

admin.site.register(Hospital)
admin.site.register(Patient)
admin.site.register(RequestAppointment)
admin.site.register(Service)
admin.site.register(Doctor)
