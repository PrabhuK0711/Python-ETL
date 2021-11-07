# Create your views here.
from django.shortcuts import render
from datalab2.models import epion_practices, epion_offices
from django.http import HttpResponse
import json
import os


def load_jason(request):
    cur_dir = os.getcwd()
    data_dir = os.path.join(cur_dir, 'data')
    os.chdir(data_dir)

    with open('offices.json') as json_data:
        offices = json.load(json_data)
    
        for row in offices:
            epion_offices.objects.create(
                epion_practice_id=row["epion_practice_id"],
                launched_date = row["launched_date"],
                disabled_date = row["disabled_date"],
                emr_department_ids = row["emr_department_ids"],
                office_name = row["office_name"]
            )
    
    with open('practices.json') as json_data:
    
        practices = json.load(json_data)
        
        for row in practices:
            epion_practices.objects.create(
                practice_name=row["practice_name"],
                emr_practice_id = row["emr_practice_id"],
                epion_practice_id = row["epion_practice_id"]
            )
            
    return HttpResponse('Data to Postgresql Loaded Successfully')