# datalab1/urls.py
from django.urls import path

from .views import data_analysis


urlpatterns = [
    path('datalab1', data_analysis, name='Data analysis - ETL')
]