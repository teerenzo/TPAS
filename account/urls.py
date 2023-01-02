from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf import settings
from . import views

urlpatterns = [
         path('',views.index),
         path('login/',views.login,name='login'),
path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
         path('signup/',views.signup,name='signup'),
         path('signup-hospital/',views.signupHospital,name='signupHospital'),
         path('dashboard/',views.dashboard,name='dashboard'),
         path('requests/',views.requests,name='requests'),
         path('getService',views.getServices,name='getService'),
         path('saveAppointment',views.saveAppointment,name='saveAppointment'),
         
         

]