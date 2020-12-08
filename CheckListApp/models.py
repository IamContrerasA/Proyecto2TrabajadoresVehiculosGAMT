from django.db import models
from TrabajadoresApp.models import Worker
from VehiculosApp.models import Vehicle

class CheckList(models.Model):
  current = models.BooleanField(default=True)  
  worker = models.ForeignKey(Worker, on_delete=models.PROTECT)
  vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)

  class Meta:
    db_table = "check_list"
