from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    APPLICANT = 1
    EMPLOYER = 2
    ROLE_CHOICES = [
        (APPLICANT,"applicant"),
        (EMPLOYER,"employer"),
    ]
    role = models.IntegerField(
        choices=ROLE_CHOICES,
        default=APPLICANT
    )

class Company(models.Model):
    user =  models.ForeignKey("User", on_delete=models.CASCADE, related_name="company_from_user")
    name = models.CharField(max_length=64)
    email = models.EmailField(max_length=64)
    phone = models.CharField(max_length=64)  

    country = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    address = models.CharField(max_length=64) 
    postal = models.CharField(max_length=64)   

    description = models.TextField()

class CV(models.Model):
    user =  models.ForeignKey("User", on_delete=models.CASCADE, related_name="CV_from_user")
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=64)
    phone = models.CharField(max_length=64)   
    
    country = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    address = models.CharField(max_length=64)   
    postal = models.CharField(max_length=64)   

    description = models.TextField()    
    text = models.TextField()    

class Education(models.Model):
    cv =  models.ForeignKey("CV", on_delete=models.CASCADE, related_name="education_from_cv")
    title = models.CharField(max_length=64)
    center = models.CharField(max_length=64)    
    start = models.DateField(null=True)
    end = models.DateField(null=True)

class Experience(models.Model):
    cv =  models.ForeignKey("CV", on_delete=models.CASCADE, related_name="experience_from_cv")
    title = models.CharField(max_length=64)
    description = models.TextField()
    start = models.DateField(null=True)
    end = models.DateField(null=True)

class Job(models.Model):
    company = models.ForeignKey("Company", on_delete=models.CASCADE, related_name="job_from_company")
    title = models.TextField()    
    description = models.TextField()    
    date = models.DateTimeField(auto_now_add=True)
    salary = models.IntegerField(null=True)
    location = models.TextField()    

class Application(models.Model):
    NOT_VIEWED = "Not Viewed"
    VIEWED = "Viewed"    
    REJECTED = "Rejected"
    CONTINUES = "Continues"
    SELECTED = "Selected"
    STATE_CHOICES = [
        (NOT_VIEWED,"Not Viewed"),
        (VIEWED,"Viewed"),        
        (REJECTED,"Rejected"),
        (CONTINUES,"Continues"),
        (SELECTED,"Selected"),
    ]
    job = models.ForeignKey("Job", on_delete=models.CASCADE, related_name="application_from_job")
    cv = models.ForeignKey("CV", on_delete=models.CASCADE, related_name="application_from_cv")
    date = models.DateTimeField(auto_now_add=True)
    letter = models.TextField()    
    state =  models.CharField(
        choices=STATE_CHOICES,
        max_length=64
    )