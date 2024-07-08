
from django.contrib.auth.models import User
from django.db import models

    
class Applicant(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    age=models.IntegerField()
    gender=models.CharField(max_length=10,choices=[('gen_male','M'),('gen_female','F')],default='gen_male')
    phone_number=models.CharField(max_length=15,null=True)
    qualification=models.CharField(max_length=100,default="")
    year_of_experience=models.IntegerField(default=0)
    job_title=models.CharField(max_length=25,blank=True,null=True)
    location=models.CharField(max_length=20,blank=True,null=True)
    resume=models.FileField(null=True,blank=True)
    
    
    def __str__(self):
        return self.name
    
class Company(models.Model):
    name = models.CharField(max_length=255)
    info = models.TextField()
    email =models.EmailField(max_length=50)
    location = models.CharField(max_length=25)
    website = models.URLField(null=True, blank=True)
    type=models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name  

class Job(models.Model):
    creator=models.ForeignKey(User,on_delete=models.CASCADE)
    company_name = models.ForeignKey(Company,on_delete=models.CASCADE)
    company_info = models.TextField()
    title= models.CharField(max_length=255)
    description=models.TextField()
    location = models.CharField(max_length=255)
    employment_type = models.CharField(max_length=50, choices=[('FT', 'Full Time'), ('PT', 'Part Time'), ('CT', 'Contract')],default='FT')
    date_posted = models.DateTimeField(auto_now_add=True)
    application_deadline = models.DateField()
    no_of_vacancy=models.IntegerField(default=0,blank=True,null=True)
    category=models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    qualification=models.CharField(max_length=100)
    experience_years=models.IntegerField(default=0)
    
    def __str__(self):
        return self.title
    

class ApplicantTracking(models.Model):
     STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('interview', 'Interview'),
        ('offered', 'Offered'),
        ('rejected', 'Rejected')
    ]
     company=models.ForeignKey(Company,on_delete=models.CASCADE)
     jobs=models.ForeignKey(Job,on_delete=models.CASCADE)
     applicant=models.ForeignKey(Applicant,on_delete=models.CASCADE)
     application_status=models.CharField(max_length=255,choices=STATUS_CHOICES, default='applied')
     applied_date=models.DateTimeField(auto_now_add=True)
     resume=models.FileField()
     cover_letter=models.FileField(null=True,blank=True)

     def __str__(self):
        return f'{self.applicant}'

