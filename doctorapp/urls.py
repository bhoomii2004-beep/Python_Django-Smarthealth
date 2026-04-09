from django.urls import path

from . import views

urlpatterns = [
    path('', views.dindex, name='dindex'),
    path('dlogin', views.dlogin, name='dlogin'),
    path('dprofile', views.dprofile, name='dprofile'),
    path('duser', views.duser, name='duser'),
    path('ddoctor', views.ddoctor, name='ddoctor'),
    path('dtreatment', views.dtreatment, name='dtreatment'),
    path('dspecialization', views.dspecialization,name='dspecialization'),
    path('dpendingappointment', views.dpendingappointment,name='dpendingappointment'),
    path('dapprovedappointment', views.dapprovedappointment,name='dapprovedappointment'),
    path('dcancelappointment', views.dcancelappointment,name='dcancelappointment'),
    path('dappointmentbill', views.dappointmentbill,name='dappointmentbill'),
    path('dtreatmentbill', views.dtreatmentbill,name='dtreatmentbill'),
    path('daddtreatment', views.daddtreatment,name='daddtreatment'),
    path('dbillgenerate', views.dbillgenerate,name='dbillgenerate'),
    path('dfeedback', views.dfeedback, name='dfeedback'),
    path('dtreatmentreport', views.dtreatmentreport, name='dtreatmentreport'),
    path('dappointmentreport', views.dappointmentreport, name='dappointmentreport'),
    path('dappointmentbillreport', views.dappointmentbillreport, name='dappointmentbillreport'),
    path('dtreatmentbillreport', views.dtreatmentbillreport, name='dtreatmentbillreport'),
    path('dlogout', views.dlogout, name='dlogout'),
    path('dedittreatment', views.dedittreatment, name='dedittreatment'),
    path('daddtreatmentbill', views.daddtreatmentbill, name='daddtreatmentbill'),
    path('daddappointmentbill', views.daddappointmentbill, name='daddappointmentbill'),
    
]  