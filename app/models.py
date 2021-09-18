from django.db import models
from authentication.models import User
# Create your models here.


gender_choices = (('Male', 'Male'), ('Female', 'Female'),('Others', 'Others'),)
reservation_category = (('SC', 'SC'), ('ST','ST'),('OBC','OBC'),('OC', 'OC'))
status_category = (('Accepted', 'Accepted'),('Pending', 'Pending'),('Rejected', 'Rejected'))

class ApplicationStatus(models.Model):
    status = models.CharField(choices=status_category,max_length=10,default="Pending")
    reason = models.TextField()
    message = models.TextField()
    apply_count = models.IntegerField(default=0)

class Application(models.Model):
    application_id = models.IntegerField()
    name = models.CharField(max_length=255)
    DoB = models.DateField()
    Aadhar = models.CharField(max_length=16)
    department = models.CharField(max_length=30,default = "select")
    specialization = models.CharField(max_length=30,default = "choose")
    Passport = models.CharField(max_length=20)
    Address = models.TextField()
    gender = models.CharField(choices=gender_choices,max_length=20)
    pwd_category = models.TextField(null=True, blank=True,max_length=255)
    documents = models.FileField(upload_to = 'documents')
    passport_pic = models.ImageField(upload_to = 'passport_pic')
    Notes = models.TextField()
    application_status = models.ForeignKey(ApplicationStatus,on_delete =models.CASCADE)
    registration_no = models.IntegerField(null=True,blank=True,unique=True)

