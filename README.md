# Requirements
- Please create a separate branch with the following naming convention: `<firstName>_<lastName>_<YYYYMMDD>`. 
- All of your work must be committed in your branch
- Every lab exercise must have a commit. Since there are 3 labs, there must be a minimum of 3 commits. Having less than
3 commits will negatively impact your evaluation
- You should be familiar with PostgreSQL database and SQL
- For this lab, you will need to set up a PostgreSQL database locally in your computer. In other words, the database host is "localhost"
- There are json files in the "data" folder that contain mock up data for this lab. Initial exercises require you to load data into your local database for later exercises
- We created the json files intentionally with missing data and mismatched data. As you go through the exercises, you will need to come up with solutions to address these irrelevant data
- All lab exercises must be solved using Python
- You may add additional libraries to solve these labs. If you do so, make sure to update the requirements.txt, so we can review the new libraries
- We will run all of your Python code using your branch. Syntax errors or missing library errors will negatively impact your evaluation
- If you are interviewing for a Coop data analyst position, you must complete the first 3 labs
- If you are interviewing for a full time data engineer position, you must complete all labs 
- Optional exercises are optional :) We recommend you complete all lab requirements before attempting optional exercises as they involve more advanced topics


# Lab setup

- We assume you already have a PostgreSQL server running in your computer for later labs
- All the following commands are to be run within your computer Terminal / Powershell
- After you clone the repository into your computer, create a new branch with the naming convention mentioned above
- Create a Python virtual environment for this project to keep this project's library dependencies clean. 
You can learn more and [set up a virtual env](https://virtualenv.pypa.io/en/latest/). The guide will help you to activate and deactivate a virtual environment. Window and Mac have different commands to use

        $ virtualenv venv

- After you activate a virtualenv within the project folder, install project dependencies 

        $ pip install -r requirements.txt

- You now have all the necessary libraries required to perform all the exercises including optional ones. 


<br>

# Background Data Explanation - MUST READ before attempting Lab1
Epion Health is a Business to Business software company. While the patients use our app to
check in before their appointments, our customers are hospitals / clinics. For the rest of this lab, 
- We refer to the hospitals / clinics as `practices`
- We refer to the medical staff who the patient meets for their appointments as `providers`
- One practice have many `children practices` because the US healthcare industry is going through many mergers and acquisitions.
- Each practice can have many physical buildings. We represent the concept using the `offices` model.
- Each practice building also have many `departments`, like family general, psychologist, etc.

As a result, in `lab1_epion_office_settings.json` file in data folder, you can see one `emr_practice_id` have 
multiple `epion_practice_id`; one `epion_practice_id` have many `offices`; one `office` has many `emr_department_id`

Practices generally only use Epion services for certain specialties because 
there are some appointments that do not require patient check in. For example, blood test or X-Ray
appointments do not need a medical check in beforehand. As a result, there are only some `emr_department_id`
are associated with epion via `lab1_epion_office_settings.json`. However, you will find many more `emr_department_id`
within `lab1_appointments.csv`. While all of these are fake data, we try to represent the actual data modeling
for your lab analysis below

# Lab 1: Data analysis - ETL

<br>

**Goals:** 


- Find all valid appointments from `lab1_appointments.csv`. Save the result as `valid_appts.csv`
- Find all valid appointments that are associated with Epion. Save the result as `epion_appts.csv`
- Calculate the Epion appointment utilization per month. Save the result as `epion_utilization`. The data set should
have the following columns: month, valid appointments associated with Epion, total valid appointments, utilization rate 


    utilization_rate = Valid Epion Appts / Total Valid Appts  

**Instructions:** 

The definition of a valid appointments is below. All conditions must match to be a valid appt

- appointment status is null **OR** appointment status does not equal "x" or does not equal "f"
- encounter_state is null **OR** encounter_state does not equal "DELETED"


Conditions for an appointment to be associated with Epion are

- Appointments with an `emr_department_id` that is specified within the Epion settings dataframe
- Appointments with appointment date >= launched_date 
- disabled date is null or appointment_date <= disabled date
- `emr_department_id` within `lab1_epion_settings.json` that has no launched date are considered not associated 
with Epion yet. Thus, appointments from those `emr_department_id` are not associated with Epion

**Notes! Sometimes there are duplicate offices for the same department due to human setup.
Make sure to calculate unique office setting for each department to determine live condition. Otherwise, you would double count those appointments
TIP: department is the logic driver here. Make sure to handle missing data**


BONUS: figure out logic to address these duplicated departments without manual data manipulation

<br>

# Lab 2: Working with a Database
Goals:
- create database tables in your local PostgreSQL database 
- upload data into these database tables

Approach and steps:
- Uploading data using Python is one of the fundamental requirements to automate all data processing 
- Please show us your Python code that uploads data
- Create a database with a name: "epiondw"
- You may choose any value for your username and password
- Make a connection to "epiondw" database 
- Create a table epion_practices with the following columns

   - practice_name: STRING
   - emr_practice_id: INTEGER
   - epion_practice_id: INTEGER

- Create a table epion_offices with the following columns

  - epion_practice_id: INTEGER
  - launched_date: DATE
  - disabled_date: DATE
  - emr_department_ids: ARRAY(INTEGER)
  - office_name: STRING

- Use Python to upload data in `practices.json` file in data folder in to practice table
- Use Python to upload data in `offices.json` file in data folder to office table


# Lab 3: Working with external system via REST API

Goals: 
- Authenticate with our interview server with the provided username and password below
- GET appointments data from `dwcore-dev.epionhealth.net/appointments/` with the authentication token retrieved from the fist step

Instructions:

- All work must be done with Python
- All API communication needs to have a header attribute: `'content-type': 'application/json'`
- First, send a POST to `dwcore-dev.epionhealth.net/api-token-auth` for a token. Pass json as the request body with
the following attributes


      {
        "username": "interview",
        "password": "goodMorning:)"
      }

- The server will reply with JSON in the following format

      {'token': '....'}

- With the token, call a GET to `dwcore-dev.epionhealth.net/appointments/` with a header including the 
following attribute

      'Authorization': "Token <token_value>"

- If done correctly, the result will reply with a paginated result. The sample schema is below. Go
through all the pages to get the entire appointment list. The appointments you retrieve are the exact data in 
`lab1_appointments.csv` in the data folder. Save your result as `rest_appointments.csv` 


      {
         "count": ...,
         "next": ...,
         "prev": ...,
         "results": [...]
      } 


# Lab 4: Tie it all together with a Django Web App

- You should already have all necessary libraries to start the web app. Go to `datalab/settings.py` file and 
update your database username and password at `DATABASES` settings

- Let's make sure you have a good starting point. Start the django server as shown below. 
A Django server should run in development mode at http://127.0.0.1:8000/. 
Checking the url, you should see a congratulation page saying the installation works

        $ python manage.py runserver

- Run the initial database set up migration. Everything should go through successfully

        $ python manage.py migrate

- You now have a working Django server / project running locally on your computer. 
Create an app within this project called "core"

- Within the core app, create a model: Task with the following schema

        - Name: Text field max length 200, null = False
        - start_time: datetime, null = False
        - end_time: datetime
        - created_at: datetime auto create
        - updated_at: datetime auto create, auto update

- Register the core app and task model with Django admin

- You can import your other lab exercises within lib folder by updating `lib/__init.py__` file

- Create an after-create trigger on the tasks model such that if a task is created with a name "lab5"
the Django server will perform the lab1 logic. Please make sure this task is only triggered for after create events. 
Django signal document is a good reference point



<br/>

# Lab 5: Optional - Send complex tasks to background with Celery
- Generally, we want to keep the django server free to process incoming requests. 
As a result, we want to push long-running tasks to a worker to perform in the background.
You can achieve this by using the `celery` library. 
- This setup will involve the following steps

  - Setting up a message queue broker (rabbitmq, etc.) on your local machine
  - Updating django setting file
  - Registering the task to celery
  - Within the "after create" code in lab 4, trigger lab1 logic to run in the background

- This is an advanced lab exercise that will clearly set your application apart from other candidates.
- Along with the code to set up celery and django, please provide instructions to set up a background worker
- We wil follow your lab5 instruction to ensure your code is working on our machine
