from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class epion_practices(models.Model):
    practice_name = models.TextField()
    emr_practice_id = models.IntegerField()
    epion_practice_id = models.IntegerField()
    class Meta:
        db_table = "epion_practices"

class epion_offices(models.Model):
    epion_practice_id = models.IntegerField()
    launched_date = models.DateField(default=None, blank=True, null=True)
    disabled_date = models.DateField(default=None, blank=True, null=True)
    emr_department_ids = ArrayField(models.IntegerField(),default=None)
    office_name = models.TextField() 
    class Meta:
        db_table = "epion_offices"