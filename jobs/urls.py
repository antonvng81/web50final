from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("applicant_access", views.applicant_access_view, name="applicant_access"),
    path("applicant_register", views.applicant_register_view, name="applicant_register"),
    path("applicant_home", views.applicant_home_view, name="applicant_home"),  
    path("applicant_job_list", views.applicant_job_list_view, name="applicant_job_list_init"),
    path("applicant_job_list/<int:page_number>", views.applicant_job_list_view, name="applicant_job_list"),  
    path("applicant_edit_cv", views.applicant_edit_cv_view, name="applicant_edit_cv"),  
    path("applicant_apply_job/<int:job_id>", views.applicant_apply_job_view, name="applicant_apply_job"),  
    path("applicant_applied_list", views.applicant_applied_list_view, name="applicant_applied_list_init"),
    path("applicant_applied_list/<int:page_number>", views.applicant_applied_list_view, name="applicant_applied_list"),

    path("employer_access", views.employer_access_view, name="employer_access"),
    path("employer_register", views.employer_register_view, name="employer_register"),    
    path("employer_home", views.employer_home_view, name="employer_home"),  
    path("employer_edit_company", views.employer_edit_company_view, name="employer_edit_company"), 
    path("employer_edit_job/<int:job_id>", views.employer_edit_job_view, name="employer_edit_job"),  
    path("employer_create_job", views.employer_create_job_view, name="employer_create_job"),
    path("employer_job_list", views.employer_job_list_view, name="employer_job_list_init"),  
    path("employer_job_list/<int:page_number>", views.employer_job_list_view, name="employer_job_list"),
    path("employer_applied_list/<int:job_id>", views.employer_applied_list_view, name="employer_applied_list_init"),  
    path("employer_applied_list/<int:job_id>/<int:page_number>", views.employer_applied_list_view, name="employer_applied_list"),  
    path("employer_edit_application/<int:application_id>", views.employer_edit_application_view, name="employer_edit_application"),

    path("applicant_create_education_api", views.applicant_create_education_api, name="applicant_create_education_api"),
    path("applicant_get_educations_api", views.applicant_get_educations_api, name="applicant_get_educations_api"),
    path("applicant_remove_education_api", views.applicant_remove_education_api, name="applicant_remove_education_api"),

    path("applicant_create_experience_api", views.applicant_create_experience_api, name="applicant_create_experience_api"),
    path("applicant_get_experiences_api", views.applicant_get_experiences_api, name="applicant_get_experiences_api"),
    path("applicant_remove_experience_api", views.applicant_remove_experience_api, name="applicant_remove_experience_api"),

    path("logout", views.logout_view, name="logout"),
    ]