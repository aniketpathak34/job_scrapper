from django.urls import path
from . import views

urlpatterns = [
    path('scrape_jobs/', views.scrape_jobs, name='scrape_jobs'),
]
