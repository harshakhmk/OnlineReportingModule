from django.urls import path
from .views import *

urlpatterns = [
    # for student user
    path('applications/',applicationsHandler,name='applications'),
    path('application-status/<int:application_id>/',applicationStatus,name='applicationStatus'),

    # Admin View
    path('accepted/',accepted_list,name='accepted-applications'),
    path('rejected/',rejected_list,name='rejected-applications'),
    path('pending/',pending_list,name='pending-applications'),

    path('pending/applications/<int:id>',pending_edit,name='pending-edit'),
]