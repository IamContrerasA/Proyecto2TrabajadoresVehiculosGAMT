from django.db import models
from AreasApp.models import Area

class Worker(models.Model):
  dni = models.CharField(max_length=8)
  username = models.CharField(max_length=100)
  email = models.EmailField()
  slept_hours = models.DecimalField(max_digits=4, decimal_places=2)
  area = models.ForeignKey(Area, on_delete=models.PROTECT)

  class Meta:
    db_table = "worker"

