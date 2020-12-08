from django.db import models
from TrabajadoresApp.models import Worker

class Fatigue(models.Model):
  slept_hours = models.DecimalField(max_digits=4, decimal_places=2)
  time_to_bed = models.DateTimeField(auto_now=False,blank=True)  
  time_to_wake = models.DateTimeField(auto_now=False,blank=True)  
  worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
  
  class Meta:
    db_table = "fatigue"

