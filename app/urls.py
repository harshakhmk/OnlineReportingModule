from django.urls import path
from .views import *

urlpatterns = [
    # for student user
    path('applications/',applicationsHandler,name='applications'),
    path('application-status/',applicationStatus,name='applicationStatus'),
    path('application_detail/<int:id>/',application_detail,name='application_detail'),
    path('',home,name="home"),
    # Admin View

    path('incoming-applications/',incoming_applications,name='incoming-applications'),
    path('pending/applications/<int:id>',pending_edit,name='pending_edit'),
]