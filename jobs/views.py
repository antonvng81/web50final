from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .util import Q_search_location, Q_search_title, Q_search_cv_text
import json

from .models import User, Company, Job, CV, Application, Education, Experience
 
# Create your views here.
def index(request):
    return render(request, "jobs/index.html",{
        "nav_items":[
            {"view":"applicant_access","text":"Applicant Access"},
            {"view":"employer_access","text":"Employer Access"},
        ]
    })

def applicant_access_view(request):
    
    nav_items = [
            {"view":"applicant_access","text":"Applicant Access","active":True},
            {"view":"employer_access","text":"Employer Access"}]

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.role == User.APPLICANT:
                login(request, user)
                return redirect(reverse("applicant_job_list_init")) #!! Change to default applicant view
            else:
                return render(request, "jobs/applicant_access.html", {
                    "message": "Invalid username and/or password.",
                    "nav_items":nav_items
                    })
        else:
            return render(request, "jobs/applicant_access.html", {
                "message": "Invalid username and/or password.",
                "nav_items":nav_items
                })
    else:
        return render(request, "jobs/applicant_access.html",{
            "nav_items":nav_items
        })

def employer_access_view(request):
    nav_items = [
            {"view":"applicant_access","text":"Applicant Access"},
            {"view":"employer_access","text":"Employer Access","active":True}]

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.role == User.EMPLOYER:
                login(request, user)
                return redirect(reverse("employer_home")) 
            else:
                return render(request, "jobs/employer_access.html", {
                    "message": "Invalid username and/or password.",
                    "nav_items":nav_items
                    })
        else:
            return render(request, "jobs/employer_access.html", {
                "message": "Invalid username and/or password.",
                "nav_items":nav_items
                })
    else:
        return render(request, "jobs/employer_access.html",{
            "nav_items":nav_items
        })

def applicant_register_view(request):

    nav_items = [
            {"view":"applicant_access","text":"Applicant Access"},
            {"view":"employer_access","text":"Employer Access"}]

    if request.method == "POST":

        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "jobs/applicant_register.html", {
                "message": "Passwords must match.",
                "nav_items": nav_items
            })

        try:
            user = User.objects.create_user(
                username=username, 
                email=email, 
                password=password,
                role=User.APPLICANT)
            user.save()

            cv = CV(user=user)
            cv.save()
            
        except IntegrityError:
            return render(request, "jobs/applicant_register.html", {
                "message": "Username already taken.",
                "nav_items": nav_items                
            })

        login(request, user)
        return redirect(reverse("applicant_home"))#!Change to default applicant view
    else:
        return render(request, "jobs/applicant_register.html", {"nav_items":nav_items})


def employer_register_view(request):

    nav_items = [ 
        {"view":"applicant_access","text":"Applicant Access"},
        {"view":"employer_access","text":"Employer Access"} ]

    if request.method == "POST":

        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "jobs/employer_register.html", {
                "message": "Passwords must match.",
                "nav_items": nav_items
            })

        try:
            user = User.objects.create_user(
                username=username,
                email=email, 
                password=password, 
                role=User.EMPLOYER)
            user.save()

            company = Company(user = user)
            company.save()

        except IntegrityError:
            return render(request, "jobs/employer_register.html", {
                "message": "Username already taken.",
                "nav_items": nav_items                
            })

        login(request, user)
        return redirect(reverse("employer_home"))
    else:
        return render(request, "jobs/employer_register.html", {"nav_items":nav_items})


def logout_view(request):
    logout(request)
    return redirect(reverse("index"))

def employer_home_view(request):
    if request.user.is_authenticated and request.user.role == User.EMPLOYER:
        nav_items = [
            {"view":"employer_job_list_init","text":"Jobs","icon":"bi-binoculars"},
            {"view":"employer_create_job","text":"Create","icon":"bi-plus-square"},
            {"view":"employer_edit_company","text":"Company","icon":"bi-building"},
            {"view":"logout","text":"Log Out","icon":"bi-box-arrow-left",} ]
        
        nav_items_left = [
            {"view":"employer_home","icon":"bi-house","text":request.user.username, "active":True}]

        try:
            company = Company.objects.get(user=request.user)
        except Company.DoesNotExist:
            return render(request, "jobs/employer_home.html", {"message":"Company is not created.", "nav_items":nav_items,"nav_items_left":nav_items_left})        
            
        return render(request, "jobs/employer_home.html", {"company":company,  "nav_items":nav_items, "nav_items_left":nav_items_left})
    else:
        
        nav_items = [ 
            {"view":"applicant_access","text":"Applicant Access"},
            {"view":"employer_access","text":"Employer Access"} ] 
        
        return render(request, "jobs/employer_home.html", {"message":"User not authenticated.", "stop_edit":True, "nav_items":nav_items})        


def employer_edit_company_view(request):

    if request.user.is_authenticated and request.user.role == User.EMPLOYER:

        nav_items = [
            {"view":"employer_job_list_init","text":"Jobs","icon":"bi-binoculars"},
            {"view":"employer_create_job","text":"Create","icon":"bi-plus-square"},
            {"view":"employer_edit_company","text":"Company","icon":"bi-building", "active":True},
            {"view":"logout","text":"Log Out","icon":"bi-box-arrow-left",} ]

        nav_items_left = [
            {"view":"employer_home","icon":"bi-house","text":request.user.username}]

        try:
            company = Company.objects.get(user=request.user)
        except Company.DoesNotExist:
            return render(request, "jobs/employer_edit_company.html", {"message":"Company is not created.", "stop_edit":True, "nav_items":nav_items,"nav_items_left":nav_items_left})        

        if request.method == "POST":

            company.name = request.POST["name"]
            company.email = request.POST["email"]
            company.phone = request.POST["phone"]
            company.country = request.POST["country"]
            company.city = request.POST["city"]
            company.postal = request.POST["postal"]
            company.address = request.POST["address"]
            company.description = request.POST["description"]                        
            
            company.save()

            return redirect(reverse("employer_home"))

        else:
            return render(request, "jobs/employer_edit_company.html", {"company":company, "stop_edit":False, "nav_items":nav_items,"nav_items_left":nav_items_left})
    else:
        nav_items = [ 
            {"view":"applicant_access","text":"Applicant Access"},
            {"view":"employer_access","text":"Employer Access"} ] 
        
        return render(request, "jobs/employer_edit_company.html", {"message":"User not authenticated.", "stop_edit":True,"nav_items":nav_items})        


def employer_edit_job_view(request, job_id):

    if request.user.is_authenticated and request.user.role == User.EMPLOYER:

        nav_items = [
            {"view":"employer_job_list","text":"Jobs","icon":"bi-arrow-left","state":request.session["employer_job_list_state"],"active":True},
            {"view":"logout","text":"Log Out","icon":"bi-box-arrow-left",} ]

        nav_items_left = [
            {"view":"employer_home","icon":"bi-house","text":request.user.username}]

        try:
            company = Company.objects.get(user=request.user)
        except Company.DoesNotExist:
            return render(request, "jobs/employer_edit_job.html", {"message":"Company is not created.", "nav_items":nav_items, "stop_edit":True,"nav_items_left":nav_items_left})        

        try:
            job = Job.objects.filter(company=company,id=job_id).first()
        except Job.DoesNotExist:
            return render(request, "jobs/employer_edit_job.html", {"message":"Wrong job id or not user owner", "nav_items":nav_items, "stop_edit":True,"nav_items_left":nav_items_left})        
    
        if request.method == "POST":

            if "save" in request.POST:

                salary = request.POST["salary"]                
                if salary == "":
                    salary = None

                job.salary = salary
                job.location = request.POST["location"]
                job.title = request.POST["title"]
                job.description = request.POST["description"]                        
                job.save()

                return redirect(reverse("employer_job_list_init"))

            if "delete" in request.POST:
                job.delete()
                return redirect(reverse("employer_job_list_init"))

            if "applications" in request.POST:
                return redirect(reverse("employer_applied_list_init",kwargs={"job_id":job.id}))

        else:
            return render(request, "jobs/employer_edit_job.html", {"nav_items":nav_items, "job":job, "stop_edit":False,"nav_items_left":nav_items_left})
    else:
        nav_items = [ 
            {"view":"applicant_access","text":"Applicant Access"},
            {"view":"employer_access","text":"Employer Access"} ] 
        
        return render(request, "jobs/employer_edit_job.html", {"message":"User not authenticated.", "nav_items":nav_items, "stop_edit":True})        


def employer_create_job_view(request):

    if request.user.is_authenticated and request.user.role == User.EMPLOYER:

        nav_items = [
            {"view":"employer_job_list_init","text":"Jobs","icon":"bi-binoculars"},
            {"view":"employer_create_job","text":"Create","icon":"bi-plus-square", "active":True},
            {"view":"employer_edit_company","text":"Company","icon":"bi-building"},
            {"view":"logout","text":"Log Out","icon":"bi-box-arrow-left",} ]

        nav_items_left = [
            {"view":"employer_home","icon":"bi-house","text":request.user.username}]

        try:
            company = Company.objects.get(user=request.user)
        except Company.DoesNotExist:
            return render(request, "jobs/employer_create_job.html", {"message":"Company is not created.", "nav_items":nav_items, "stop_edit":True,"nav_items_left":nav_items_left})        

        if request.method == "POST":

            
            salary = request.POST["salary"]
            if salary=='':
                salary = None

            job = Job(
                date = timezone.now(),
                company = company,
                salary = salary,
                location = request.POST["location"],
                title = request.POST["title"],
                description = request.POST["description"] 
                )
            job.save()

            return redirect(reverse("employer_job_list_init"))

        else:
            return render(request, "jobs/employer_create_job.html", {"nav_items":nav_items, "stop_edit":False,"nav_items_left":nav_items_left})
    else:
        nav_items = [
            {"view":"applicant_access","text":"Applicant Access"},
            {"view":"employer_access","text":"Employer Access"} ] 
        
        return render(request, "jobs/employer_create_job.html", {"message":"User not authenticated.", "nav_items":nav_items, "stop_edit":True})        

def employer_job_list_view(request, page_number=1):
        
    if request.user.is_authenticated and request.user.role == User.EMPLOYER:

        nav_items = [
            {"view":"employer_job_list_init","text":"Jobs","icon":"bi-binoculars", "active":True},
            {"view":"employer_create_job","text":"Create","icon":"bi-plus-square"},
            {"view":"employer_edit_company","text":"Company","icon":"bi-building"},
            {"view":"logout","text":"Log Out","icon":"bi-box-arrow-left",} ]

        nav_items_left = [
            {"view":"employer_home","icon":"bi-house","text":request.user.username}]

        request.session["employer_job_list_state"] = (page_number,)

        try:
            company = Company.objects.get(user=request.user)
        except Company.DoesNotExist:
            return render(request, "jobs/employer_job_list.html", {"message":"Company is not created.", "nav_items":nav_items, "stop_edit":True,"nav_items_left":nav_items_left})        

        objects = Job.objects.filter(company=company).order_by('-date')
        paginator = Paginator(objects,10)
        page_obj = paginator.page(page_number)

        return render(request, "jobs/employer_job_list.html",{"count":objects.count(),"page": page_obj, "nav_items":nav_items, "stop_edit":False,"nav_items_left":nav_items_left})

    else:
        nav_items = [ 
            {"view":"applicant_access","text":"Applicant Access"},
            {"view":"employer_access","text":"Employer Access"} ] 
        
        return render(request, "jobs/employer_job_list.html", {"message":"User not authenticated.", "nav_items":nav_items, "stop_edit":True})   


def applicant_job_list_view(request, page_number=1):
        
    if request.user.is_authenticated and request.user.role == User.APPLICANT:

        nav_items = [
            {"view":"applicant_job_list_init","text":"Jobs","icon":"bi-binoculars", "active":True},
            {"view":"applicant_applied_list_init","text":"Applied","icon":"bi-briefcase",},
            {"view":"applicant_edit_cv","text":"CV","icon":"bi-person",},            
            {"view":"logout","text":"Log Out","icon":"bi-box-arrow-left",} ]

        nav_items_left = [
            {"view":"applicant_home","icon":"bi-house","text":request.user.username}]

        if "applicant_job_list_title" in request.session:
            search_title = request.session["applicant_job_list_title"]
        else:
            search_title = ""

        if "applicant_job_list_location" in request.session:
            search_location = request.session["applicant_job_list_location"]
        else:
            search_location = ""

        if request.method == "POST":
            if "search-title" in request.POST:
                search_title = request.POST.get("search-title")
                search_location = request.POST.get("search-location")
                request.session["applicant_job_list_title"] = search_title
                request.session["applicant_job_list_location"] = search_location
                page_number = 1

        # BASIC SEARCH ALGORITHM

        if search_title == None or search_title =="":
            if search_location is not None and search_location != "":
                objects = Job.objects.filter(Q_search_location(search_location)).order_by('-date')
            else:
                objects = Job.objects.all().order_by('-date')
        
        else:
            if search_location is not None and search_location != "":
                objects = Job.objects.filter(Q_search_title(search_title),Q_search_location(search_location)).order_by('-date')
            else:
                objects = Job.objects.filter(Q_search_title(search_title)).order_by('-date')

        request.session["applicant_job_list_state"] = (page_number,)
        request.session["applicant_applied_list_state"] = (1,)

        paginator = Paginator(objects,10)
        page_obj = paginator.page(page_number)

        return render(request, "jobs/applicant_job_list.html",{"search_location":search_location,"search_title":search_title, 
        "count":objects.count(),"page": page_obj, "nav_items":nav_items, "stop_edit":False,"nav_items_left":nav_items_left})
    else:
        nav_items = [ 
            {"view":"applicant_access","text":"Applicant Access"},
            {"view":"employer_access","text":"Employer Access"} ] 
        
        return render(request, "jobs/applicant_job_list.html", {"message":"User not authenticated.", "nav_items":nav_items, "stop_edit":True})

def applicant_edit_cv_view(request):

    if request.user.is_authenticated and request.user.role == User.APPLICANT:

        nav_items = [
            {"view":"applicant_job_list_init","text":"Jobs","icon":"bi-binoculars"},
            {"view":"applicant_applied_list_init","text":"Applied","icon":"bi-briefcase",},
            {"view":"applicant_edit_cv","text":"CV","icon":"bi-person","active":True},
            {"view":"logout","text":"Log Out","icon":"bi-box-arrow-left",} ]

        nav_items_left = [
            {"view":"applicant_home","icon":"bi-house","text":request.user.username}]

        try:
            cv = CV.objects.get(user=request.user)
        except CV.DoesNotExist:
            return render(request, "jobs/applicant_edit_cv.html", {"message":"CV text is not created.", "stop_edit":True, "nav_items":nav_items,"nav_items_left":nav_items_left})        

        if request.method == "POST":

            cv.first_name = request.POST["first_name"]
            cv.last_name = request.POST["last_name"]
            cv.email = request.POST["email"]
            cv.phone = request.POST["phone"]
            cv.country = request.POST["country"]
            cv.city = request.POST["city"]
            cv.address = request.POST["address"]
            cv.postal = request.POST["postal"]
            cv.description = request.POST["description"]
            cv.text = request.POST["text"]                                    
            
            cv.save()

            return render(request, "jobs/applicant_edit_cv.html", {"cv":cv, "stop_edit":False, "nav_items":nav_items,"nav_items_left":nav_items_left})

        else:
            return render(request, "jobs/applicant_edit_cv.html", {"cv":cv, "stop_edit":False, "nav_items":nav_items,"nav_items_left":nav_items_left})
    else:
        nav_items = [ 
            {"view":"applicant_access","text":"Applicant Access"},
            {"view":"employer_access","text":"Employer Access"} ] 
        
        return render(request, "jobs/applicant_edit_cv.html", {"message":"User not authenticated.", "stop_edit":True,"nav_items":nav_items})        

def applicant_home_view(request):

    if request.user.is_authenticated and request.user.role == User.APPLICANT:
        
        nav_items = [
            {"view":"applicant_job_list_init","text":"Jobs","icon":"bi-binoculars"},
            {"view":"applicant_applied_list_init","text":"Applied","icon":"bi-briefcase",},
            {"view":"applicant_edit_cv","text":"CV","icon":"bi-person",},
            {"view":"logout","text":"Log Out","icon":"bi-box-arrow-left",} ]
        
        nav_items_left = [
            {"view":"applicant_home","icon":"bi-house","text":request.user.username, "active":True}]

        try:
            cv = CV.objects.get(user=request.user)
        except CV.DoesNotExist:
            return render(request, "jobs/applicant_home.html", {"message":"CV text is not created.", "stop_edit":False, "nav_items":nav_items,"nav_items_left":nav_items_left})        
            
        educations = Education.objects.filter(cv=cv).order_by('-end')
        if not educations.exists():
            educations=None

        experiences = Experience.objects.filter(cv=cv).order_by('-end')
        if not experiences.exists():
            experiences=None

        return render(request, "jobs/applicant_home.html", {"cv":cv, "educations":educations,"experiences":experiences, "nav_items":nav_items, "nav_items_left":nav_items_left})
    else:
        
        nav_items = [ 
            {"view":"applicant_access","text":"Applicant Access"},
            {"view":"employer_access","text":"Employer Access"} ] 
        
        return render(request, "jobs/applicant_home.html", {"message":"User not authenticated.", "stop_edit":True,"nav_items":nav_items})        

def applicant_apply_job_view(request, job_id):

    if request.user.is_authenticated and request.user.role == User.APPLICANT:
    
        nav_items = [
            {"view":"applicant_job_list","text":"Jobs","icon":"bi-arrow-left","active":True, "state":request.session["applicant_job_list_state"]},
            {"view":"applicant_applied_list","text":"Applied","icon":"bi-arrow-left", "state":request.session["applicant_applied_list_state"]},
            {"view":"logout","text":"Log Out","icon":"bi-box-arrow-left",} ]
        
        nav_items_left = [
            {"view":"applicant_home","icon":"bi-house","text":request.user.username}]

        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return render(request, "jobs/applicant_apply_job.html", {"message":"Job doesn't exists.", "stop_edit":True, "nav_items":nav_items,"nav_items_left":nav_items_left})        
         
        try:
            cv = CV.objects.get(user=request.user)
        except CV.DoesNotExist:
            return render(request, "jobs/applicant_apply_job.html", {"message":"CV text is not created.", "stop_edit":True, "nav_items":nav_items,"nav_items_left":nav_items_left})        
                

        try:
            already_applied = Application.objects.filter(job=job, cv=cv).first()
        except Application.DoesNotExist:
            already_applied = None

        if request.method == "POST" and not already_applied:
            
            letter = request.POST["letter"]
         
            application = Application(
                job=job,
                cv=cv,
                date=timezone.now(),
                letter=letter,
                state=Application.NOT_VIEWED
            )
            application.save()

            return redirect(reverse("applicant_job_list", args=request.session["applicant_job_list_state"]))
        else:
            count = Application.objects.filter(job=job).count()
            return render(request, "jobs/applicant_apply_job.html", {"count":count,"already_applied":already_applied, "job":job,  "nav_items":nav_items, "nav_items_left":nav_items_left})
    else:
        
        nav_items = [ 
            {"view":"applicant_access","text":"Applicant Access"},
            {"view":"employer_access","text":"Employer Access"} ] 
        
        return render(request, "jobs/applicant_home.html", {"message":"User not authenticated.", "company":None,"nav_items":nav_items})        

def employer_applied_list_view(request, job_id, page_number=1):
        
    if request.user.is_authenticated and request.user.role == User.EMPLOYER:
        nav_items = [
            {"view":"employer_job_list","text":"Jobs","icon":"bi-arrow-left","state":request.session["employer_job_list_state"],"active":True},            
            {"view":"logout","text":"Log Out","icon":"bi-box-arrow-left",} ]

        nav_items_left = [
            {"view":"employer_home","icon":"bi-house","text":request.user.username}]

        # SEARCH ALGORITHM

        if "employer_applied_list_search_state" in request.session:
            search_state = request.session["employer_applied_list_search_state"]
        else:
            search_state = "All"

        if "employer_applied_list_search_cv" in request.session:
            search_cv = request.session["employer_applied_list_search_cv"]
        else:
            search_cv = ""

        if request.method == "POST":
            if "search_state" in request.POST:
                search_cv = request.POST.get("search_cv")
                search_state =  request.POST.get("search_state")
                request.session["employer_applied_list_search_state"] = search_state
                request.session["employer_applied_list_search_cv"] = search_cv
                page_number = 1

        if search_cv == "" or search_cv is None:
            if search_state == "All" or search_state is None:
                objects = Application.objects.filter(job__id=job_id).order_by('-date')
            else:
                objects = Application.objects.filter(job__id=job_id,state=search_state).order_by('-date')
        else:
            if search_state == "All" or search_state is None:
                objects = Application.objects.filter(Q_search_cv_text(search_cv),job__id=job_id).order_by('-date')
            else:
                objects = Application.objects.filter(Q_search_cv_text(search_cv),job__id=job_id,state=search_state).order_by('-date')


        request.session["employer_applied_list_state"] = (job_id, page_number)

        paginator = Paginator(objects,10)
        page_obj = paginator.page(page_number)

        return render(request, "jobs/employer_applied_list.html",{"search_state":search_state,"search_cv":search_cv,"count":objects.count(),"page": page_obj, "job_id":job_id, "nav_items":nav_items, "stop_edit":False,"nav_items_left":nav_items_left})

    else:
        nav_items = [ 
            {"view":"applicant_access","text":"Applicant Access"},
            {"view":"employer_access","text":"Employer Access"} ] 
        
        return render(request, "jobs/employer_applied_list.html", {"message":"User not authenticated.", "nav_items":nav_items, "stop_edit":True})


def employer_edit_application_view(request, application_id):
        
    if request.user.is_authenticated and request.user.role == User.EMPLOYER:

        nav_items = [
            {"view":"employer_applied_list","text":"Applicants","icon":"bi-arrow-left","state":request.session["employer_applied_list_state"],"active":True},            
            {"view":"logout","text":"Log Out","icon":"bi-box-arrow-left",} ]

        nav_items_left = [
            {"view":"employer_home","icon":"bi-house","text":request.user.username}]


        try:
            application = Application.objects.get(id=application_id)
        except Application.DoesNotExist:
            return render(request, "jobs/employer_edit_application.html",{"message":"Application doesn't exists", "nav_items":nav_items, "stop_edit":True,"nav_items_left":nav_items_left})


        if request.method == "POST":                       
            application.state = request.POST["state"]
            application.save()
            return redirect(reverse("employer_applied_list", args=request.session["employer_applied_list_state"]))
        else:
            if application.state == Application.NOT_VIEWED:
                application.state = Application.VIEWED
                application.save()

        cv = application.cv

        educations = Education.objects.filter(cv=cv).order_by('-end')
        if not educations.exists():
            educations = None

        experiences = Experience.objects.filter(cv=cv).order_by('-end')
        if not experiences.exists():
            experiences = None

        return render(request, "jobs/employer_edit_application.html",{"state":application.state, "experiences":experiences,"educations":educations,"cv":cv, "application":application, "nav_items":nav_items, "stop_edit":False,"nav_items_left":nav_items_left})

    else:
        nav_items = [ 
            {"view":"applicant_access","text":"Applicant Access"},
            {"view":"employer_access","text":"Employer Access"} ] 
        
        return render(request, "jobs/employer_edit_application.html", {"message":"User not authenticated.", "nav_items":nav_items, "stop_edit":True})

def applicant_applied_list_view(request, page_number=1):
        
    if request.user.is_authenticated and request.user.role == User.APPLICANT:
        nav_items = [
            {"view":"applicant_job_list_init","text":"Jobs","icon":"bi-binoculars"},
            {"view":"applicant_applied_list_init","text":"Applied","icon":"bi-briefcase","active":True},
            {"view":"applicant_edit_cv","text":"CV","icon":"bi-person",},
            {"view":"logout","text":"Log Out","icon":"bi-box-arrow-left",} ]
        
        nav_items_left = [
            {"view":"applicant_home","icon":"bi-house","text":request.user.username}]

        request.session["applicant_applied_list_state"] = (page_number,)
        request.session["applicant_job_list_state"] = (1,)

        objects = Application.objects.filter(cv__user__id=request.user.id).order_by('-date')
        paginator = Paginator(objects,10)
        page_obj = paginator.page(page_number)

        return render(request, "jobs/applicant_applied_list.html",{"count":objects.count(),"page": page_obj, "nav_items":nav_items, "nav_items_left":nav_items_left})

    else:
        nav_items = [ 
            {"view":"applicant_access","text":"Applicant Access"},
            {"view":"employer_access","text":"Employer Access"} ] 
        
        return render(request, "jobs/applicant_applied_list.html", {"message":"User not authenticated.", "nav_items":nav_items, "stop_edit":True})

@csrf_exempt
def applicant_create_education_api(request):

    if request.user.is_authenticated and request.user.role == User.APPLICANT:
        if request.method != "POST":
            return JsonResponse({"error": "POST request required."}, status=400)
        else:

            try:
                cv = CV.objects.get(user=request.user)
            except CV.DoesNotExist:
                return JsonResponse({"error": "CV doesn't exists."}, status=400)

            data = json.loads(request.body)

            start = data.get('start',None)
            if start == '':
                start = None

            end = data.get('end',None)
            if end == '':
                end = None

            education = Education(
                cv = cv,
                title = data.get('title',''),
                center = data.get('center',''),
                start = start,
                end = end
                )

            education.save()

            return JsonResponse({"message": "Education created."}, status=201)
    else:
        return JsonResponse({"error":"User not authenticated."}, status=403)


@csrf_exempt
def applicant_get_educations_api(request):

    if request.user.is_authenticated and request.user.role == User.APPLICANT:

        if request.method != "POST":
            return JsonResponse({"error": "POST request required."}, status=400)
        else:           
            objects = Education.objects.filter(cv__user=request.user).order_by('-end')
            educations = [{
                "title":object.title,
                "center":object.center,
                "start":object.start,
                "end":object.end,
                "id":str(object.id)}
                for object in objects]

            return JsonResponse({"message": "Education object send successfully.","educations":educations}, status=200)        
    else:
        return JsonResponse({"error": "User not authenticated."}, status=403)  

@csrf_exempt
def applicant_remove_education_api(request):

    if request.user.is_authenticated and request.user.role == User.APPLICANT:

        if request.method != "POST":
            return JsonResponse({"error": "POST request required."}, status=400)
        else:     
            data = json.loads(request.body)
            education_id = data.get('id')

            try:
                education = Education.objects.get(id=education_id)
            except Education.DoesNotExist:
                return JsonResponse({"error": "Education doesn't exists."}, status=400)

            education.delete()

            return JsonResponse({"message": "Education object removed successfully."}, status=200)        
    else:
        return JsonResponse({"error": "User not authenticated."}, status=403)  



@csrf_exempt
def applicant_create_experience_api(request):

    if request.user.is_authenticated and request.user.role == User.APPLICANT:
        if request.method != "POST":
            return JsonResponse({"error": "POST request required."}, status=400)
        else:

            try:
                cv = CV.objects.get(user=request.user)
            except CV.DoesNotExist:
                return JsonResponse({"error": "CV doesn't exists."}, status=400)

            data = json.loads(request.body)

            start = data.get('start',None)
            if start == '':
                start = None

            end = data.get('end',None)
            if end == '':
                end = None

            experience = Experience(
                cv = cv,
                title = data.get('title',''),
                description = data.get('description',''),
                start = start,
                end = end
                )

            experience.save()

            return JsonResponse({"message": "Experience created."}, status=201)
    else:
        return JsonResponse({"error":"User not authenticated."}, status=403)


@csrf_exempt
def applicant_get_experiences_api(request):

    if request.user.is_authenticated and request.user.role == User.APPLICANT:

        if request.method != "POST":
            return JsonResponse({"error": "POST request required."}, status=400)
        else:           
            objects = Experience.objects.filter(cv__user=request.user).order_by('-end')
            experiences = [{
                "title":object.title,
                "description":object.description,
                "start":object.start,
                "end":object.end,
                "id":str(object.id)}
                for object in objects]

            return JsonResponse({"message": "Experience object send successfully.","experiences":experiences}, status=200)        
    else:
        return JsonResponse({"error": "User not authenticated."}, status=403)  

@csrf_exempt
def applicant_remove_experience_api(request):

    if request.user.is_authenticated and request.user.role == User.APPLICANT:

        if request.method != "POST":
            return JsonResponse({"error": "POST request required."}, status=400)
        else:     
            data = json.loads(request.body)
            experience_id = data.get('id')

            try:
                experience = Experience.objects.get(id=experience_id)
            except Experience.DoesNotExist:
                return JsonResponse({"error": "Experience doesn't exists."}, status=400)

            experience.delete()

            return JsonResponse({"message": "Experience object removed successfully."}, status=200)        
    else:
        return JsonResponse({"error": "User not authenticated."}, status=403)  