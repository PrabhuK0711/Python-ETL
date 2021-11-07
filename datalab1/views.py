from django.shortcuts import render
from django.http import HttpResponse
import os
import pandas as pd
import json


def valid_appt(df):
    valid_appt_ids = []

    for (idx, row) in df.iterrows():
        if (not row.appointment_status or row.appointment_status not in ('x', 'f')) and \
                (not row.encounter_status or row.encounter_status != 'DELETED'):
            valid_appt_ids.append(row.emr_appointment_id)
    
    # Filter the appointments with the valid appt IDs
    df_valid = df[df['emr_appointment_id'].isin(valid_appt_ids)]
    # Write the records to the output file
    df_valid.to_csv('valid_appts.csv', index=False)

def valid_epion_appt(df):
    with open('lab1_epion_office_settings.json') as json_data:
        office_setting = json.load(json_data)

    emr_dept_ids = []
    # Dictionary to store the key value pairs for department ID and value as a tuple of launch_date, disabled_date
    # of the office
    dept_off_dict = {}

    for i in office_setting:
        launch_date = i['launched_date']
        disabled_date = i['disabled_date']

        if i['launched_date']:
            if isinstance(i['emr_department_ids'], list) :
                emr_dept_ids += i['emr_department_ids']
                for dept in i['emr_department_ids']:
                    dept_off_dict[dept] = (launch_date, disabled_date)
            else:
                dept = i['emr_department_ids']
                dept_off_dict[dept] = (launch_date, disabled_date)
                emr_dept_ids += [dept]
    
    # Filter the appointments with only the emr_department_ids from the json office setting file
    df_epion_appt = df[df['emr_department_id'].isin(emr_dept_ids)]
    
    dept_ids = df_epion_appt['emr_department_id'].to_list()
    appt_dates = df_epion_appt['appointment_date'].to_list()
    appt_ids = df_epion_appt['emr_appointment_id'].to_list()

    # To filter appointment IDs based on launch date <= appointment date <= disabled date logic
    valid_appt_ids = []
    for i in range(len(df_epion_appt.index)):
        dept = dept_ids[i]
        launch = dept_off_dict[dept][0]
        disabled = dept_off_dict[dept][1]
        appt_date = appt_dates[i]
        appt_id = appt_ids[i]

        if launch <= appt_date and (not disabled or appt_date <= disabled):
            valid_appt_ids.append(appt_id)
    
    # Filter the dataframe using valid appointment IDs
    df_epion_appt = df_epion_appt[df_epion_appt['emr_appointment_id'].isin(valid_appt_ids)]
    df_epion_appt.to_csv('epion_appts.csv', index=False)

def data_analysis(request):
    cur_dir = os.getcwd()
    data_dir = os.path.join(cur_dir, 'data')
    os.chdir(data_dir + '\\')
    
    df = pd.read_csv('lab1_appointments.csv')

    valid_appt(df)
    valid_epion_appt(df)    

    return HttpResponse('Data Analysis Completed Successfully')