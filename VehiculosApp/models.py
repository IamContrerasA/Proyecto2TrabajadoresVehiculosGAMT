from django.db import models

class Vehicle(models.Model):
  unit_code = models.CharField(max_length=20)
  plate_number = models.CharField(max_length=20)
  year = models.IntegerField()
  brand = models.CharField(max_length=50)
  color = models.CharField(max_length=50)
  model = models.CharField(max_length=50)  

  class Meta:
    db_table = "vehicle"

