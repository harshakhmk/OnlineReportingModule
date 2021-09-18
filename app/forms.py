from django import forms
from .models import Application, ApplicationStatus

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('application_id','name','DoB','Aadhar','department','specialization','Passport','Address','gender','pwd_category','documents','passport_pic','Notes')


class ApplicationStatusForm(forms.ModelForm):
    registration_no = forms.IntegerField()
    class Meta:
        model = ApplicationStatus
        fields = ('status','reason','message','registration_no')