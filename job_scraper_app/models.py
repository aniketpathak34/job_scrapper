from django.db import models

class Job(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=200)
    company_name  = models.CharField(max_length=200)
    company_location = models.CharField(max_length=100)
    company_salary = models.CharField(max_length=100, default="Salary not disclosed")

    def __str__(self):
        return self.title
