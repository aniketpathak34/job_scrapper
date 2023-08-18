from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('id', 'company_name', 'company_location', 'title')
    # list_editable = ('company_location', 'company_salary', 'title')
