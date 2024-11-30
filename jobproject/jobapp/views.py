from django.shortcuts import render,redirect, get_object_or_404,reverse
from django.http import HttpResponse,HttpResponseForbidden, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User,Permission
from  .models import Applicant,Job,ApplicantTracking,Company
from .import models,forms
from .forms import CompanyForm,ApplicantForm,JobForm,ApplicantTrackingForm
from django.conf import settings 
from django.core.mail import send_mail
from .utils import send_job_notifications
from django.urls import reverse_lazy,reverse
from django.views.generic.edit import UpdateView
from django.db.models import Q
from django.templatetags.static import static
from django.core.mail.message import EmailMessage
from django.core.exceptions import ObjectDoesNotExist

def index(request):
    return render(request,'index.html')

def applicantlogin_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('/admin/')  
            else:
                login(request, user)
                return redirect('applicanthome')  
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('applicantlogin')
    return render(request, 'applicantlogin.html')

def companylogin_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('/admin/')  
            else:
                login(request, user)
                return redirect('companyhome') 
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('companylogin')
    return render(request, 'companylogin.html')

def logout_view(request):
    logout(request)
    return redirect('index')

def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('emailid')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'sign_up.html', {'error': "Passwords do not match."})

        if User.objects.filter(email=email).exists():
            return render(request, 'sign_up.html', {'error': "A user with the same email already exists."})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'sign_up.html', {'error': "Username already exists."})

        user = User.objects.create_user(email=email, username=username, password=password)
        user.save()
        messages.success(request, f'Account created for {username}!')
        return redirect('index')

    return render(request, 'sign_up.html')

def applicant_home(request):
    user = request.user
    try:
        applicant = Applicant.objects.get(user=user)
    except Applicant.DoesNotExist:
        applicant = None
    if applicant and applicant.job_title:
        matching_jobs = Job.objects.filter(title__icontains=applicant.job_title, location__icontains=applicant.location)
        other_jobs = Job.objects.exclude(title__icontains=applicant.job_title, location__icontains=applicant.location)
    else:
        matching_jobs=Job.objects.all()
        other_jobs = Job.objects.none()

    jobs = list(matching_jobs) + list(other_jobs)
    return render(request, 'applicant_home.html', {'jobs': jobs, 'applicant': applicant})

def job_details(request, id):
    job = get_object_or_404(Job, id=id)
    return render(request, 'jobdetails.html', {'job': job})

def company_home(request):
    jobs = Job.objects.filter(creator=request.user)
    matching_applicants = Applicant.objects.none()
    all_applicants = Applicant.objects.all()

    if jobs.exists():
        for job in jobs:
            job_matching_applicants = Applicant.objects.filter(job_title=job.title, qualification=job.qualification,location=job.location)
            matching_applicants = matching_applicants | job_matching_applicants

    non_matching_applicants = all_applicants.exclude(id__in=matching_applicants.values_list('id', flat=True))

    context = {
        'jobs': jobs,
        'matching_applicants': matching_applicants,
        'non_matching_applicants': non_matching_applicants
    }

    if request.method == 'POST':
        try:
            company = Company.objects.get(user=request.user)
        except Company.DoesNotExist:
            return redirect('companyform')  
        applicant_id = request.POST.get('applicant_id')
        applicant = Applicant.objects.get(id=applicant_id)
        
        
        send_mail(
            'Job Opportunity',
            f'Hi {applicant.name},\n\nWe are interested in your profile for the {applicant.job_title} position at {company.name}. Please contact us for further discussion.\n\nBest regards,\nYour Company',
            settings.DEFAULT_FROM_EMAIL,
            [applicant.user.email],
            fail_silently=False,
        )
        return redirect('companyhome')
    return render(request, 'company_home.html', context)

def applicant_details(request, id):
    applicant = get_object_or_404(Applicant, id=id)
    return render(request, 'applicantdetails.html', {'applicant': applicant})

def applicant_form_view(request):
    already_submitted = Applicant.objects.filter(user=request.user).exists()
    
    if already_submitted:
        return render(request, 'applicant_form.html', {'already_submitted': True})
    
    if request.method == 'POST':
        form = ApplicantForm(request.POST, request.FILES)
        if form.is_valid():
            applicant = form.save(commit=False)
            applicant.user = request.user  
            applicant.save()
            return redirect('applicanthome')  
    else:
        form = ApplicantForm()
    
    return render(request, 'applicant_form.html', {'form': form})

def applicantprofile_view(request):
    applicant = Applicant.objects.filter(user=request.user)
    if not applicant.exists():
        return render(request, "error_appl.html")
    try:
        applicant = Applicant.objects.get(user=request.user)
    except Applicant.DoesNotExist:
        applicant = Applicant(user=request.user)
    if request.method == "POST":
        form = ApplicantForm(request.POST, request.FILES, instance=applicant)
        if form.is_valid():
            form.save()
            return redirect('applicantprofile') 
        editable = True 
    else:
        form = ApplicantForm(instance=applicant)
        editable = 'edit' in request.GET 
    context = {
        'form': form,
        'editable': editable 
    }
    return render(request, "appl_profile.html", context)

def companyprofile_view(request):
    company = Company.objects.filter(user=request.user)
    if not company.exists():
        return render(request, "error_com.html")
    try:
        company = Company.objects.get(user=request.user)
    except Company.DoesNotExist:
        company = Company(user=request.user)
    if request.method == "POST":
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            return redirect('companyprofile') 
        editable = True
    else:
        form = CompanyForm(instance=company)
        editable = 'edit' in request.GET 
    context = {
        'form': form,
        'editable': editable 
    }
    return render(request, "comp_profile.html", context)


def post_job_view(request):
    company = Company.objects.filter(user=request.user)
    if not company.exists():
        return render(request, "error_com.html")
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.creator = request.user  
            job.company = company.first()  
            job.save()
            send_job_notifications(job.id)  
            return redirect('companyhome')  
    else:
        form = JobForm()
    return render(request, 'postjob.html', {'form': form})


def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'job_list.html', {'jobs': jobs})

def company_jobs_list(request):
    jobs = Job.objects.filter(creator=request.user)
    return render(request, 'companyjobs.html', {'jobs': jobs})
   
def delete_job_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if job.creator != request.user:
        return HttpResponseForbidden("You do not have permission to delete this job.")
    job.delete()
    return redirect('companyjobs')


class JobUpdateView(UpdateView):
    model = Job
    form_class = JobForm
    template_name = 'editjob.html'
    success_url = reverse_lazy('companyjobs')

    def get_queryset(self):
        return Job.objects.filter(creator=self.request.user)

    def form_valid(self, form):
        if form.instance.creator != self.request.user:
            return HttpResponseForbidden()
        return super().form_valid(form)

def applyjob_view(request, job_id): 
    job = get_object_or_404(Job, id=job_id) 
    applicant_user = request.user  
    try:
        applicant = Applicant.objects.get(user=applicant_user)
    except Applicant.DoesNotExist:
        return redirect('applicantform')  

    if request.method == 'POST':
        form = ApplicantTrackingForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.jobs = job  
            application.company = job.company_name 
            application.applicant = applicant  
            application.application_status = 'Pending' 
            application.save()

            send_application_notification_email(
                company=application.company, 
                job=application.jobs, 
                applicant=application.applicant
            )

            return redirect('joblist')  
    else:
        form = ApplicantTrackingForm()

    return render(request, 'apply_job.html', {'form': form})

def send_application_notification_email(company, job,applicant):
    subject = f'New Job Application for {job.title} at {company.name}'
    message=( 
        f"Hi {company.name},\n\n"
        f"An applicant named{applicant.name}that matches your qualifications has applied for :\n\n"
        f"Title: {job.title}\n"
        f"Description: {job.description}\n\n"
        f"Best regards,\nYour Job Board Team"
    )
    from_email = 'demoidlubi@gmail.com'  
    to_email = company.user.email  
    try:
        email = EmailMessage(subject, message, from_email, [to_email])
        if applicant.resume:
            email.attach(applicant.resume.name, applicant.resume.read(), applicant.resume.content_type)
        if applicant.cover_letter:
            email.attach(applicant.cover_letter.name, applicant.cover_letter.read(), applicant.cover_letter.content_type)
        
        email.send(fail_silently=False)  

    except Exception as e:
        print(f"Error sending email: {str(e)}")

def applicant_jobs_view(request):
    try:
        applicant = Applicant.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return redirect('errorappl')  
    applied_jobs = ApplicantTracking.objects.filter(applicant=applicant).select_related('jobs', 'company')

    return render(request, 'appliedjobs.html', {'applied_jobs': applied_jobs})

def company_form_view(request):
    already_submitted = Company.objects.filter(user=request.user).exists()
    
    if already_submitted:
        return render(request, 'company_form.html', {'already_submitted': True})
    
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.user = request.user  
            company.save()
            return redirect('companyhome')
    else:
        form = CompanyForm()
    return render(request, 'company_form.html', {'form': form})

def view_applicants(request):
    try:
        company = Company.objects.get(user=request.user)
    except Company.DoesNotExist:
        messages.error(request, "You do not have permission to view these applicants.")
        return redirect('errorcomp')

    if request.method == "POST":
        applicant_id = request.POST.get('applicant_id')
        new_status = request.POST.get('application_status')
        send_email = request.POST.get('send_email') == "true"
        try:
            application = ApplicantTracking.objects.get(id=applicant_id, company=company)
            application.application_status = new_status
            application.save()
            if send_email:
                subject = f"Application Status Update for {application.jobs.title}"
                message = (
                    f"Dear {application.applicant.name},\n\n"
                    f"Your application for the position of {application.jobs.title} at {company.name} has been updated.\n"
                    f"New Status: {new_status}\n\n"
                    f"Thank you for applying with us.\n\n"
                    f"more details will be send later"
                    f"Best regards,\n{company.name} Team"
                   
                )
                from_email = "demoidlubi@gmail.com"
                to_email = application.applicant.user.email
                send_mail(subject, message, from_email, [to_email])

                messages.success(request, f"Status updated and email sent to {application.applicant.name}.")
            else:
                messages.success(request, f"Status updated for {application.applicant.name}.")
        except ApplicantTracking.DoesNotExist:
            messages.error(request, "Application not found or you don't have permission to update this application.")

        return redirect('viewapplicants')

    applicants = ApplicantTracking.objects.filter(company=company)
    return render(request, 'view_applicants.html', {'company': company, 'applicants': applicants})

def companies_with_jobs(request):
    companies = Company.objects.all()
    companies_jobs = []
    for company in companies:
        jobs = Job.objects.filter(company_name=company)
        companies_jobs.append({
            'company': company,
            'jobs': jobs
        })

    context = {
        'companies_jobs': companies_jobs
    }
    return render(request, 'company&jobs.html', context)

def view_jobs(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    jobs = Job.objects.filter(company_name=company)

    context = {
        'company': company,
        'jobs': jobs
    }
    return render(request, 'view_jobs.html', context)

def search_jobs(request):
    query = request.GET.get('q')
    if query:
        job_listings = Job.objects.filter(title__icontains=query) | Job.objects.filter(description__icontains=query) | Job.objects.filter(company_name__name__icontains=query) | Job.objects.filter(location__icontains=query) | Job.objects.filter(category__icontains=query)
        
    else:
        job_listings = Job.objects.all()
    return render(request, 'searchjobs.html', {'job_listings': job_listings, 'query': query})


def search_applicants(request):
    query = request.GET.get('qu')
    if query:
        applicants = Applicant.objects.filter(
            qualification__icontains=query
        ) | Applicant.objects.filter(
            job_title__icontains=query
        ) | Applicant.objects.filter(
            location__icontains=query
        )
    else:
        applicants = Applicant.objects.all()
    
    if request.method == 'POST':
        try:
            company = Company.objects.get(user=request.user)
        except Company.DoesNotExist:
            return redirect('companyform')  
        applicant_id = request.POST.get('applicant_id')
        applicant = Applicant.objects.get(id=applicant_id)
        
        # Sending the email
        send_mail(
            'Job Opportunity',
            f'Hi {applicant.name},\n\nWe are interested in your profile for the {applicant.job_title} position at {company.name}. Please contact us for further discussion.\n\nBest regards,\nYour Company',
            settings.DEFAULT_FROM_EMAIL,
            [applicant.user.email],
            fail_silently=False,
        )
        return redirect('searchapplicants')
    
    return render(request, 'searchapplicants.html', {'Applicants': applicants, 'query': query})

    
def errorcomp_view(request):
    return render(request,'error_com.html')

def errorappl_view(request):
    return render(request,'error_appl.html')

def aboutus_view1(request):
    return render(request,'aboutus1.html')

def contactus_view1(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name = sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(
                subject=f'{name} || {email}',
                message=message,
                from_email=request.user.email,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False
            )
            return redirect('applicanthome') 
        else:
            return render(request, 'contactus1.html', {'form': sub, 'success': False})
    return render(request, 'contactus1.html', {'form': sub})

def resetPassword(request):
    if request.method == "POST":
        uname = request.POST.get('uname')
        newpwd = request.POST.get('password')
        
        if uname and newpwd:
            try:
                user = User.objects.get(username=uname)
                user.set_password(newpwd)
                user.save()
                return render(request, "ResetPassword.html", {"errmsg": "Password reset successfully"})
            except User.DoesNotExist:
                return render(request, "ResetPassword.html", {"errmsg": "User does not exist"})
            except Exception as e:
                print(e)
                return render(request, "ResetPassword.html", {"errmsg": "Password reset failed"})
        else:
            return render(request, "ResetPassword.html", {"errmsg": "Please provide both username and password"})
    return render(request, "ResetPassword.html")

def aboutus_view2(request):
    return render(request,'aboutus2.html')

def contactus_view2(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name = sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(
                subject=f'{name} || {email}',
                message=message,
                from_email=request.user.email,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False
            )
            return redirect('companyhome') 
        else:
            return render(request, 'contactus2.html', {'form': sub, 'success': False})
    return render(request, 'contactus2.html', {'form': sub})
