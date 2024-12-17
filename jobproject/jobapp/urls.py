from django.contrib import admin
from django.urls import path
from .import views
from .views import JobUpdateView, job_list
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    
    path('', views.index, name='index'),
    path('admin_home',views.admin_home,name='adminhome'),
    path('admin_applicants',views.admin_applicantsview,name='adminapplicants'),
    path('admin_companies',views.admin_companiesview,name='admincompanies'),
    path('admin_users',views.admin_usersview,name='allusers'),
    path('applicantogin',views.applicantlogin_view,name='applicantlogin'),
    path('companylogin',views.companylogin_view,name='companylogin'),
    path('sign_up', views.signup_view, name='sign_up'), 
    path('Logout/', views.logout_view, name='Logout'),
    path('reset',views.resetPassword,name='reset'),
    path('applicantform',views.applicant_form_view,name='applicantform'),
    path('companyform',views.company_form_view, name='companyform'),
    path('companyhome', views.company_home, name='companyhome'),
    path('applicant/<int:id>/', views.applicant_details, name='applicant_details'),
    path('companies_jobs/',views.companies_with_jobs, name='companiesjobs'),
    path('applicanthome', views.applicant_home, name='applicanthome'),
    path('job/<int:id>/', views.job_details, name='job_details'),
    path('applicantprofile', views.applicantprofile_view, name='applicantprofile'),
    path('companyprofile', views.companyprofile_view, name='companyprofile'),
    path('postjob',views.post_job_view,name='postjob'),
    path('joblist', views.job_list, name='joblist'),
    path('companyjobs', views.company_jobs_list, name='companyjobs'),
    path('company/<int:company_id>/jobs/', views.view_jobs, name='view_jobs'),
    path('joblist/delete/<int:job_id>/', views.delete_job_view, name='delete_job'),
    path('joblist/edit/<int:pk>/', JobUpdateView.as_view() , name='edit_job'),
    path('apply/<int:job_id>/', views.applyjob_view, name='apply_job'),
    path('my-applied-jobs/', views.applicant_jobs_view, name='appliedjobs'),
    path('viewapplicants', views.view_applicants, name='viewapplicants'),
    path('searchjobs', views.search_jobs, name='searchjobs'),
    path('searchapplicants', views.search_applicants, name='searchapplicants'),
    path('errorcomp',views.errorcomp_view,name='errorcomp'),
    path('errorappl',views.errorappl_view,name='errorappl'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('aboutus1', views.aboutus_view1, name='aboutus1'),
    path('contactus1/', views.contactus_view1, name='contactus1'),
    path('aboutus2', views.aboutus_view2, name='aboutus2'),
    path('contactus2/', views.contactus_view2, name='contactus2'),
    
]

#+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

 