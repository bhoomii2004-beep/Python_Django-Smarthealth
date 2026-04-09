from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('specialization', views.specialization, name='specialization'),
    path('specializationedit', views.specializationedit, name='specializationedit'),
    path('feedback', views.feedback, name='feedback'),
    path('user', views.user, name='user'),
    path('userdetails', views.userdetails, name='userdetails'),
    path('doctor', views.doctor, name='doctor'),
    path('pendingappointment', views.pendingappointment, name='pendingappointment'),
    path('approvedappointment', views.approvedappointment, name='approvedappointment'),
    path('cancelappointment', views.cancelappointment, name='cancelappointment'),
    path('treatment', views.treatment, name='treatment'),
    path('treatmentbill', views.treatmentbill, name='treatmentbill'),
    path('appointmentbill', views.appointmentbill, name='appointmentbill'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('appointmentreport', views.appointmentreport, name='appointmentreport'),
    path('treatmentreport', views.treatmentreport, name='treatmentreport'),
    path('appointmentbillreport', views.appointmentbillreport, name='appointmentbillreport'),
    path('treatmentbillreport', views.treatmentbillreport, name='treatmentbillreport'),
    path('changepassword', views.changepassword, name='changepassword'),
]  