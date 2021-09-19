from django.shortcuts import render,redirect,get_list_or_404, get_object_or_404
from .models import Application
from authentication.models import User
# Create your views here.
from django.contrib import messages
from .forms import ApplicationForm,ApplicationStatusForm
from utils.permissions import student_required,admin_required
from utils.email  import Util


def applicationsHandler(request):
    if request.method =='GET':
        form = ApplicationForm()
        return render(request, "application_form.html",{'form':form})
    else: # POST method
        form = ApplicationForm(request.POST, request.FILES)
        apps_obj = list(Application.objects.filter(applicationId = request.POST.get('applicationId','')))
        print(len(apps_obj))
        if len(apps_obj)==0 or apps_obj[-1].status == "Rejected":
             # new application here
             if form.is_valid() :
                 form.save()
                 print("Application submitted successfully")
                 messages.success(request,"Your application successfully submitted")
                 return redirect('/')   # Mention url name here
             else :
                 print(form.errors)
                 messages.error(request,"Invalid data")
                 return redirect("applications")

        else:
            status = apps_obj[-1].status
            messages.error(request,f" your status is {status}, Please wait for sometime")
            return redirect('applicationStatus')#"application-status")

def applicationStatus(request):
    id = -1
    if request.GET.get('applicationId') is not None:
        id = int(request.GET.get('applicationId'))
    obj=[]


    if id !=-1:
        obj = list(Application.objects.filter(applicationId=id))
    status = ""
    if len(obj) > 0:
        status = obj[-1].status
        messages.success(request,f" Your recent application status is {status}")
    else:
        messages.info(request, "You haven't applied yet")
        status = "Not applied yet"
    return render(request,"appStatus.html",{"status":status,"message":f"Your application status is {status}"})




@admin_required(login_url='accounts/login')
def application_detail(request,id):
    obj = get_object_or_404(Application, id=id)
    return render(request,"application_detail.html",{"app":obj})

@admin_required(login_url='accounts/login')
def incoming_applications(request):
    if request.method == 'GET':
        accepted = Application.objects.filter(status="Accepted")
        rejected = Application.objects.filter(status="Rejected")
        pending = Application.objects.filter(status="Pending")
        return render(request,"admin.html",{'accepted':accepted, 'rejected':rejected, 'pending':pending})
    elif request.method == 'POST':

        id = request.POST.get('id')
        application = get_object_or_404(Application,id=id)
        form = ApplicationStatusForm(request.POST)
        print("form data is stored in above variable")
        if form.is_valid():
            print("valid form in pending update")

            if request.POST.get('status','') == "Accepted":
                reg_no = request.POST.get('registration_no')
                print("Status accepted")
                if Application.objects.filter(registration_no=reg_no).exists():
                    messages.error(request,f"{reg_no} Already exists")
                    print("But registration  is already exists,try new")
                    return redirect("pending_edit")
                else:
                    application.registration_no = reg_no
                    application.save()
                    application.status = "Accepted"
                    application.save()
                    email_data = {"subject":"Your application is accepted","body":f"Application is accepted and {reg_no} is Registration Number","to_email":"kharshakashyap@gmail.com"}
                    Util.send_email(email_data)
                    print("Registration number updated")
            elif request.POST.get('status','') == "Rejected":
                application.reason = request.POST.get('reason','')
                print("Rejected application, check again")
                application.save()
                application.status = "Rejected"
                application.save()

            messages.success(request,f" Your application was {application.status}")
            return redirect("incoming-applications")
        else:# invalid data
            messages.error(request,"Error in data")
            print("Errors in your data")
            print(form.errors)
            return redirect("incoming-applications")

@admin_required(login_url='accounts/login')
def pending_edit(request,id):
    application = get_object_or_404(Application,id=id)
    form = ApplicationStatusForm()
    if request.method == 'GET':
        return render(request, 'admin.html')
    elif request.method == 'POST':
        form = ApplicationStatusForm(request.POST)
        print("form data is stored in above variable")
        if form.is_valid():
            print("valid form in pending update")

            if request.POST.get('status','') == "Accepted":
                reg_no = request.POST.get('registration_no')
                print("Status accepted")
                if Application.objects.filter(registration_no=reg_no).exists():
                    messages.error(request,f"{reg_no} Already exists")
                    print("But registration  is already exists,try new")
                    return redirect("pending_edit")
                else:
                    application.registration_no = reg_no
                    email_data = {"subject":"Your application is accepted","body":f"Application is accepted and {reg_no} is Registration Number","to_email":"kharshakashyap@gmail.com"}
                    Util.send_email(email_data)
                    print("Registration number updated")
            elif request.POST.get('status','') == "Rejected":
                application.reason = request.POST.get('reason','')
                print("Rejected application, check again")
            application.save()
            messages.success(request,f" Your application was {application.status}")
            return redirect("incoming-applications")
        else:# invalid data
            messages.error(request,"Error in data")
            print("Errors in your data")
            return redirect("incoming-applications")

    else: # GET method
        return render(request,"admin.html",{'form':form})


def home(request):
    if request.user.is_authenticated():
        return render(request,"index.html")
    return redirect('applications')