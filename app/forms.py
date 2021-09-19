from django import forms
from .models import Application

class ApplicationForm(forms.ModelForm):
    """
    documents = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )
    passport_pic = forms.ImageField(label='Select a file',
        help_text='max. 42 megabytes')
    """
    class Meta:
        model = Application
        fields = ('applicationId','name','DoB','Aadhar','department','specialization','Passport','Address','gender','reservation_category','pwd_category','documents','passport_pic','Notes')


class ApplicationStatusForm(forms.ModelForm):
    registration_no = forms.IntegerField(required=False)
    class Meta:
        model = Application
        fields = ('status','reason','registration_no')