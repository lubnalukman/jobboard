from collections.abc import Sequence
from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from .models import*

class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name', 'location', 'date_posted', 'creator')
    search_fields = ('title', 'company_name', 'location')

class ApplicantTrackingAdmin(admin.ModelAdmin):
    list_display = ('jobs', 'applicant', 'application_status', 'applied_date')
    search_fields = ('jobs__title', 'applicant__username')
    list_filter = ('application_status',)

class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
    search_fields = ('user__username', 'phone_number')

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'location', 'website', 'type', 'user')
    search_fields = ('name', 'email', 'location', 'type')
    list_filter = ('type', 'location')


admin.site.register(Job, JobAdmin)
admin.site.register(ApplicantTracking, ApplicantTrackingAdmin)
admin.site.register(Applicant, ApplicantAdmin)
admin.site.register(Company, CompanyAdmin)



        
