from django.urls import path
from .views import *

urlpatterns = [
    # for student user
    path('applications/',applicationsHandler,name='applicationsHandler'),
    path('application-status/',applicationStatus,name='applicationStatus'),

    # Admin View
    path('accepted/',accepted_list,name='accepted-applications'),
    path('rejected/',rejected_list,name='rejected-applications'),
    path('pending/',pending_list,name='pending-applications'),

    path('accepted/applications/<int:id>/',accepted_edit,name='accepted-edit'),
    path('rejected/applications/<int:id>',rejected_edit,name='rejected-edit'),
    path('pending/applications/<int:id>',pending_edit,name='pending-edit'),
]