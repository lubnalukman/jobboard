# utils.py

from .models import Job, Applicant
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Company, Job, ApplicantTracking

def send_job_notifications(job_listing_id):
    job_listing = Job.objects.get(id=job_listing_id)
    applicants = Applicant.objects.all()

    for applicant in applicants:
        if match_qualifications(job_listing.qualification, applicant.qualification):
            send_notification_email(applicant, job_listing)

def match_qualifications(required, provided):
    required_set = set(required.split(','))
    provided_set = set(provided.split(','))
    return required_set.issubset(provided_set)

def send_notification_email(applicant, job_listing):
    subject = f"New Job Listing: {job_listing.title}"
    message = (
        f"Hi {applicant.name},\n\n"
        f"A new job listing that matches your qualifications has been posted:\n\n"
        f"Title: {job_listing.title}\n"
        f"Description: {job_listing.description}\n\n"
        f"Best regards,\nYour Job Board Team"
    )
    send_mail(subject, message, 'demoidlubi@gmail.com', [applicant.user.email])


 