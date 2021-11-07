# datalab2/urls.py
from django.urls import path

from .views import load_jason


urlpatterns = [
    path('', load_jason, name='JSON LOAD to POSTGRESQL')
]