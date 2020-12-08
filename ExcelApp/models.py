from django.db import models

class Excel(models.Model):
  name = models.CharField(max_length=100)
  file = models.FileField(upload_to='files/excels/')
  created_at = models.DateTimeField(auto_now=True)  
  state = models.CharField(max_length=1, default="0")
  
  class Meta:
    db_table = "excel"

class Contratista(models.Model):  
  name = models.CharField(max_length=200) 

  class Meta:
    db_table = "contratista"

class Transporte(models.Model):
  name = models.CharField(max_length=200)   

  class Meta:
    db_table = "transporte"
  
class ModalidadIngreso(models.Model):
  name = models.CharField(max_length=200)   

  class Meta:
    db_table = "modalidad_ingreso"

class TipoVehiculo(models.Model):
  name = models.CharField(max_length=200)   

  class Meta:
    db_table = "tipo_vehiculo"

class Carga(models.Model):
  name = models.CharField(max_length=200)   

  class Meta:
    db_table = "carga"

class Destino(models.Model):
  name = models.CharField(max_length=200)   

  class Meta:
    db_table = "destino"
    
class NumConvoy(models.Model):
  name = models.CharField(max_length=200)   

  class Meta:
    db_table = "num_convoy"

class Estado(models.Model):
  name = models.CharField(max_length=200)   

  class Meta:
    db_table = "estado"

class Motivo(models.Model):
  name = models.CharField(max_length=200)   

  class Meta:
    db_table = "motivo"

class Conductor(models.Model):
  name = models.CharField(max_length=200) 
  dni = models.CharField(max_length=20, null = True)   
  license = models.CharField(max_length=20)   

  class Meta:
    db_table = "conductor"

class ConductorArchivos(models.Model):
  conductor = models.ForeignKey(Conductor, on_delete=models.CASCADE)  
  fatiga_file = models.CharField(max_length=200)  
  fatiga_file_encode = models.TextField(null=True)
  declaracion_file = models.CharField(max_length=200)
  declaracion_file_encode = models.TextField(null=True)  
  iperc_file = models.CharField(max_length=200)  
  iperc_file_encode = models.TextField(null=True)
  date = models.CharField(max_length=10)  
  
  class Meta:
    db_table = "conductor_archivos"

class Placa(models.Model):
  placa1 = models.CharField(max_length=100) 
  placa2 = models.CharField(max_length=100)    

  class Meta:
    db_table = "placa"

class PlacaArchivos(models.Model):
  placa = models.ForeignKey(Placa, on_delete=models.CASCADE)  
  checklist_file = models.CharField(max_length=200)
  checklist_file_encode = models.TextField(null=True)
  date = models.CharField(max_length=10)  
  
  class Meta:
    db_table = "placa_archivos"

class ProgramacionGeneral(models.Model):
  ea = models.CharField(max_length=10, null=True)   
  excel = models.ForeignKey(Excel, on_delete=models.PROTECT, null=True)
  contratista = models.ForeignKey(Contratista, on_delete=models.PROTECT, null=True)
  transporte = models.ForeignKey(Transporte, on_delete=models.PROTECT, null=True)
  modalidad_ingreso = models.ForeignKey(ModalidadIngreso, on_delete=models.PROTECT, null=True)
  tipo_vehiculo = models.ForeignKey(TipoVehiculo, on_delete=models.PROTECT, null=True)
  conductor_placa = models.ForeignKey(Placa, on_delete=models.PROTECT, related_name='conductor_placa', null=True)
  conductor = models.ForeignKey(Conductor, on_delete=models.PROTECT, related_name='conductor', null=True)
  conductor_relevo = models.ForeignKey(Conductor, on_delete=models.PROTECT, related_name='conductor_relevo', null=True)  
  conductor_relevo_placa = models.ForeignKey(Placa, on_delete=models.PROTECT, related_name='conductor_relevo_placa', null=True)
  telefono_escolta = models.CharField(max_length=200, null=True)   
  telefono_satelital = models.CharField(max_length=200, null=True)  
  pasajeros = models.CharField(max_length=200, null=True)   
  carga = models.ForeignKey(Carga, on_delete=models.PROTECT, null=True)
  num_guia = models.CharField(max_length=200, null=True)   
  descripcion = models.CharField(max_length=200, null=True)   
  desde = models.ForeignKey(Destino, on_delete=models.PROTECT, related_name='desde', null=True)
  hacia = models.ForeignKey(Destino, on_delete=models.PROTECT, related_name='hacia', null=True)
  fecha_llegada = models.CharField(max_length=200, null=True)   
  hora_llegada = models.CharField(max_length=200, null=True)  
  hora_partida = models.CharField(max_length=200, null=True)  
  num_convoy = models.ForeignKey(NumConvoy, on_delete=models.PROTECT, null=True)
  eta_site = models.CharField(max_length=200, null=True)  
  estado = models.ForeignKey(Estado, on_delete=models.PROTECT, null=True)
  motivo = models.ForeignKey(Motivo, on_delete=models.PROTECT, null=True)

  class Meta:
    db_table = "programacion_general"

class Categoria(models.Model):
  name = models.CharField(max_length=100)

  class Meta:
    db_table = "categoria"

class Lugar(models.Model):
  name = models.CharField(max_length=100)

  class Meta:
    db_table = "lugar"

class Observaciones(models.Model):

  programacion_general_id = models.ForeignKey(ProgramacionGeneral, on_delete=models.PROTECT, null=True)
  descripcion = models.CharField(max_length=250, null=True)
  accion_plan = models.CharField(max_length=250, null=True)
  estado = models.ForeignKey(Estado, on_delete=models.PROTECT, null=True)
  evidencia = models.CharField(max_length=200, null=True)
  evidencia_encode = models.TextField(null=True)
  evidencia_correctiva = models.CharField(max_length=200, null=True)  
  evidencia_correctiva_encode = models.TextField(null=True)
  date = models.CharField(max_length=10, null=True)  
  categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, null=True)
  lugar = models.ForeignKey(Lugar, on_delete=models.PROTECT, null=True)

  class Meta:
    db_table = "observaciones"

