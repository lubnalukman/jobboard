from django.contrib import admin
from django.urls import path
from .import views
from .views import JobUpdateView, job_list
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    
    path('', views.index, name='index'),
    path('applicantogin',views.applicantlogin_view,name='applicantlogin'),
    path('companylogin',views.companylogin_view,name='companylogin'),
    path('sign_up', views.signup_view, name='sign_up'), 
    path('Logout/', views.logout_view, name='Logout'),
    path('reset',views.resetPassword,name='reset'),
    path('applicantform',views.applicant_form_view,name='applicantform'),
    path('companyform',views.company_form_view, name='companyform'),
    path('companyhome', views.company_home, name='companyhome'),
    path('companies_jobs/',views.companies_with_jobs, name='companiesjobs'),
    path('applicanthome', views.applicant_home, name='applicanthome'),
    path('applicantprofile', views.applicantprofile_view, name='applicantprofile'),
    path('companyprofile', views.companyprofile_view, name='companyprofile'),
    path('postjob',views.post_job_view,name='postjob'),
    path('joblist', views.job_list, name='joblist'),
    path('companyjobs', views.company_jobs_list, name='companyjobs'),
    path('company/<int:company_id>/jobs/', views.view_jobs, name='view_jobs'),
    path('joblist/delete/<int:job_id>/', views.delete_job_view, name='delete_job'),
    path('joblist/edit/<int:pk>/', JobUpdateView.as_view() , name='edit_job'),
    path('applyjob', views.applyjob_view, name='applyjob'),
    path('viewapplicants', views.view_applicants, name='viewapplicants'),
    path('searchjobs', views.search_jobs, name='searchjobs'),
    path('searchapplicants', views.search_applicants, name='searchapplicants'),
    path('errorcomp',views.errorcomp_view,name='errorcomp'),
    path('errorappl',views.errorappl_view,name='errorappl'),
    path('aboutus', views.aboutus_view, name='aboutus'),
    path('contactus/', views.contactus_view, name='contactus'),
]

#+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

 