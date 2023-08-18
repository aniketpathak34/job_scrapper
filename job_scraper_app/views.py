from django.shortcuts import render
from django.http import JsonResponse
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from .models import Job
import numpy as np


def calculate_average_salary():
    # Query the database to retrieve salary values
    salaries = Job.objects.values_list('company_salary', flat=True)

    # Convert salaries to numerical values
    numeric_salaries = []
    for salary in salaries:
        # Split the salary by dash
        parts = salary.split('-')
        
        # Process each part and extract numeric values
        for part in parts:
            numeric_text = ''.join(filter(str.isdigit, part))
            try:
                salary_value = int(numeric_text)
                numeric_salaries.append(salary_value)
            except ValueError:
                # If conversion fails, skip this part
                pass

    # Calculate the average salary using NumPy
    average_salary = np.mean(numeric_salaries)
    
    
    
    return average_salary






def scrape_jobs(request):
    average_salary = calculate_average_salary() 
    salaries = []
    # Initialize the WebDriver (you need to have the appropriate browser driver installed)
    driver = webdriver.Chrome()  # You can use other drivers like Firefox or Edge

    url = "https://in.indeed.com/jobs?q=python+developer&l=navi+mumbai%2C+maharashtra&from=searchOnHP&vjk=f34e3de8b2c4cb4b"

    driver.get(url)

    # Wait for the page to load and JavaScript to execute
    driver.implicitly_wait(10)  # Adjust the waiting time as needed

    # Get the page source with the dynamic content loaded
    page_source = driver.page_source

    # Perform further parsing using BeautifulSoup on the page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    the_name_of_tag = 'jobCard_mainContent'
    tables = soup.find_all('table', class_=the_name_of_tag)

    jobs_saved = []
    for table in tables:
        job_data = {}

        a_elements = table.find_all('a')
        for a in a_elements:
            a_id = a.get('id')
            job_data['id'] = a_id

            # Check if the job with the given ID already exists in the database
            if not Job.objects.filter(id=a_id).exists():
                div_class_to_find = 'companyName'
                div_elements = table.find_all('span', class_=div_class_to_find)
                for div in div_elements:
                    job_data['company_name'] = div.get_text()

                div_class = 'companyLocation'
                div_companylocation = table.find_all('div', class_=div_class)
                for div in div_companylocation:
                    job_data['company_location'] = div.get_text()

                div_company_salary = 'metadata salary-snippet-container'
                div_companysalary = table.find_all('div', class_=div_company_salary)
                for div in div_companysalary:
                    job_data['company_salary'] = div.get_text()
                    salary_text = div.get_text()
                    salary_value = int(''.join(filter(str.isdigit, salary_text)))
                    salaries.append(salary_value)
                average_salary = np.mean(salaries)
                print(f"The average salary for Python developers in your city is: ₹{average_salary:.2f}")


                span_elements = table.find_all('span', title=True)
                for span in span_elements:
                    job_data['title'] = span['title']

                 # If company salary data is not available, use the default value
                if 'company_salary' not in job_data:
                    job_data['company_salary'] = "Salary not disclosed"

                # Save the job data to the database
                job = Job(
                    id=job_data['id'],
                    company_name=job_data['company_name'],
                    company_location=job_data['company_location'],
                    company_salary=job_data['company_salary'],
                    title=job_data['title']
                )
                job.save()

                jobs_saved.append(job_data)

     # Call the function


    return render(request, 'job_list.html', {'jobs': jobs_saved, 'average_salarys':average_salary})





