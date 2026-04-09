from django.urls import path

from . import views

urlpatterns = [
    path('', views.uindex, name='uindex'),
    path('ulogin', views.ulogin, name='ulogin'),
    path('ucontact', views.ucontact, name='ucontact'),
    path('resendotp', views.resendotp, name='resendotp'),
    path('dresendotp', views.dresendotp, name='dresendotp'),
    path('uabout', views.uabout, name='uabout'),
    path('udoctor', views.udoctor, name='udoctor'),
    path('udocdetails', views.udocdetails, name='udocdetails'),
    path('uprofile', views.uprofile, name='uprofile'),
    path('usignup', views.usignup, name='usignup'),
    path('dsignup', views.dsignup, name='dsignup'),
    path('umyappointment', views.umyappointment, name='umyappointment'),
    path('uappointmentbill', views.uappointmentbill, name='uappointmentbill'),
    path('umytreatment', views.umytreatment, name='umytreatment'),
    path('utreatmentbill', views.utreatmentbill, name='utreatmentbill'),
    path('uterms', views.uterms, name='uterms'),
    path('uaboutcard', views.uaboutcard, name='uaboutcard'),
    path('ulogout', views.ulogout, name='ulogout'),
    path('uforgotpassword', views.uforgotpassword, name='uforgotpassword'),
    path('dforgotpassword', views.dforgotpassword, name='dforgotpassword'),


    
]  