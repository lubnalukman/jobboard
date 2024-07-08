from django import forms
from django.contrib.auth.models import User
from .import models
from .models import Company
from .models import ApplicantTracking
from .models import Applicant
from .models import Job



class ApplicantForm(forms.ModelForm):
   
    class Meta:
        model = Applicant
        fields = [
            'user',
            'name', 'age', 'gender', 'phone_number', 
            'qualification', 'year_of_experience','job_title','location','resume'
        ]
        widgets = {
            'gender': forms.RadioSelect(choices=[('gen_male', 'Male'), ('gen_female', 'Female')]),
            'job_title': forms.TextInput(attrs={'placeholder': 'Looking for the job'}),
        
        }


class JobForm(forms.ModelForm):
    CATEGORY_CHOICES = [
        ('IT', 'Information Technology (IT)'),('Healthcare', 'Healthcare'),('Finance', 'Finance'),
        ('Education', 'Education'),('Manufacturing', 'Manufacturing'),('Retail', 'Retail'),
        ('Transportation', 'Transportation'),('Construction', 'Construction'),
        ('Real_Estate', 'Real Estate'),('Hospitality', 'Hospitality'),
        ('Media_Entertainment', 'Media and Entertainment'),('Energy', 'Energy')
        ,('Telecommunications', 'Telecommunications'),('Agriculture', 'Agriculture'),
        ('Aerospace', 'Aerospace'),('Automotive', 'Automotive'),('Biotechnology', 'Biotechnology'),
        ('Consulting', 'Consulting'),('Food_Beverage', 'Food and Beverage'), ('Legal_Services', 'Legal Services'),
    ]
   
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
   
    class Meta:
        model = Job
        fields = [
            'creator','company_name','company_info','title','description','location','employment_type','application_deadline','category','salary','qualification','experience_years','no_of_vacancy'
        ]
        widgets = {
            'application_deadline': forms.DateInput(attrs={'type': 'date'}),
            'salary': forms.NumberInput(attrs={'step': 0.01}),
        }

class CompanyForm(forms.ModelForm):
    TYPE_CHOICES = [
        ('IT', 'Information Technology (IT)'),('Healthcare', 'Healthcare'),('Finance', 'Finance'),('Education', 'Education'),
        ('Manufacturing', 'Manufacturing'),('Retail', 'Retail'),('Transportation', 'Transportation'),('Construction', 'Construction'),
        ('Real_Estate', 'Real Estate'),('Hospitality', 'Hospitality'),('Media_Entertainment', 'Media and Entertainment'),('Energy', 'Energy'),
        ('Telecommunications', 'Telecommunications'), ('Agriculture', 'Agriculture'),('Aerospace', 'Aerospace'), ('Automotive', 'Automotive'),
        ('Biotechnology', 'Biotechnology'), ('Consulting', 'Consulting'),('Food_Beverage', 'Food and Beverage'),('Legal_Services', 'Legal Services'),
    ]
    type = forms.ChoiceField(choices=TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    info = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 10,'cols':10}))  # Adjust rows as needed
    class Meta:
        model = Company
        fields = ['user','name', 'info', 'email', 'location', 'website', 'type']


class ApplicantTrackingForm(forms.ModelForm):
    class Meta:
        model = ApplicantTracking
        fields = ['company', 'jobs', 'applicant', 'application_status', 'resume', 'cover_letter']
        widgets = {
            'application_status': forms.Select(choices=ApplicantTracking.STATUS_CHOICES),

        }
        

class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 5, 'cols': 30}))

