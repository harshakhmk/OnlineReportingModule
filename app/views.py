from django.shortcuts import render,get_list_or_404, get_object_or_404
from .models import Application,ApplicationStatus
# Create your views here.
from .forms import ApplicationForm
from utils.permissions import student_required,admin_required
from utils.email  import Util


def applicationsHandler(request):
    if request.method =='GET':
        form = ApplicationForm()
        return render(request, 'application-form.html',{'form':form})
    else: # POST method
        form = ApplicationForm(request.POST or None)
        apps_obj = list(Application.objects.filter(application_id = form.get('application_id')))
        if len(apps_obj)==0 or apps_obj[-1].application_status.status == "Rejected":
             # new application here
             if form.is_valid() :
                 form.save()
                 messages.success(request,"Your application successfully submitted")
                 return redirect('')   # Mention url name here
             else :
                 messages.error(request,"Invalid data")
                 return redirect("applications")

        else:
            status = apps_obj[-1].application_status.status
            messages.error(request,f" your status is {status}, Please wait for sometime")
            return redirect('applicationStatus')#"application-status")

def applicationStatus(request,application_id):
    obj = list(ApplicationStatus.objects.filter(application_id=application_id))
    status = obj.application_status.status
    if len(obj) > 0:
        messages.success(request,f" Your recent application status is {status}")
    else:
        messages.info(request, "You haven't applied yet")
    return render(request,"appStatus.html",{"status":status})



@admin_required(login_url='accounts/login')
def accepted_list(request):
    objects = Application.objects.filter(application_status__status__contains="Accepted")
    return render(request,"accepted_list.html",{'accepted_applications':objects})

@admin_required(login_url='accounts/login')
def rejected_list(request):
    objects = Application.objects.filter(application_status__status__contains="Rejected")
    return render(request,"accepted_list.html",{'accepted_applications':objects})

@admin_required(login_url='accounts/login')
def pending_list(request):
    objects = Application.objects.filter(application_status__status__contains="Pending")
    return render(request,"accepted_list.html",{'accepted_applications':objects})

@admin_required(login_url='accounts/login')
def pending_edit(request,id):
    application = get_object_or_404(Application,id=id)
    form = ApplicationStatusForm()
    if request.method == 'POST':
        form = ApplicationStatusForm(request.POST or None)
        if form.is_valid():
            application_status_obj,created = ApplicationStatus.objects.create(status=form.get('status',""),reason=form.get('reason',""),message=form.get('message',""))
            application.application_status = application_status_obj
            if application_status_obj.status == "Accepted":
                if Application.objects.filter(registration_no=form.get('registration_no',"")).exists():
                    messages.error(request,f"{form.get('registration_no')} Already exists")
                    return redirect("pending-edit")
                else:
                    application.registration_no = form.get('registration_no',"")
            application.save()
            messages.success(request,f" Your application was {application_status_obj.status}")
            return redirect("pending-applications")
        else:# invalid data
            messages.error(request,"Error in data")

    else: # GET method
        return render(request,"pending_edit.html",{'form':form})
