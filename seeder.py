from UsuariosApp.models import User, Role, UserType
from AreasApp.models import Area
from EmpresasApp.models import Company
from VehiculosApp.models import Vehicle
from TrabajadoresApp.models import Worker
from FatigasApp.models import Fatigue
from CheckListApp.models import CheckList
from ExcelApp.models import Categoria, Lugar

from django.contrib.auth.hashers import make_password

Role(name='Administrador').save()
Role(name='Supervisor').save()
Role(name='Seguridad').save()
Role(name='Trabajador').save()

Area(name='Sin Asignar').save()
Area(name='Mantenimiento').save()
Area(name='Desarrollo').save()

Company(name='Empresa 1').save()
Company(name='Empresa 2').save()

Vehicle(unit_code = 'V001', plate_number = 'XYZ-123', year = 1999, brand = 'Ford', color = 'Rojo', model = 'F-150').save()

User(dni='13579246', username='Administrador Nombre', password=make_password('Administrador1*'), role_id = 1).save()
UserType(dni='13579246', username='Administrador Nombre', password=make_password('Administrador1*'), role_id = 1).save()

Worker(dni='24681357', username='Conductor Nombre', slept_hours = 0, area_id=1).save()
UserType(dni='24681357', username='Conductor Nombre', password=make_password('Conductor1*'), role_id = 4).save()

Fatigue(slept_hours = '5.5', time_to_bed = '2020-10-19 06:17:00-05', time_to_wake = '2020-10-19 11:47:00-05', worker_id = 1).save()
Fatigue(slept_hours = '3.5', time_to_bed = '2020-10-20 06:17:00-05', time_to_wake = '2020-10-20 11:47:00-05', worker_id = 1).save()
Fatigue(slept_hours = '6.5', time_to_bed = '2020-10-21 06:17:00-05', time_to_wake = '2020-10-21 11:47:00-05', worker_id = 1).save()
Fatigue(slept_hours = '5.5', time_to_bed = '2020-10-22 06:17:00-05', time_to_wake = '2020-10-22 11:47:00-05', worker_id = 1).save()

CheckList(worker_id = 1, vehicle_id = 1).save()

Categoria(name = 'DOCUMENTACION').save()
Categoria(name = 'MTC').save()
Categoria(name = 'TRINCA').save()
Categoria(name = 'COVID-19').save()

Lugar(name = 'CHECK POINT').save()
Lugar(name = 'MAIN ACCESS ROAD').save()
Lugar(name = 'PAMPA CUELLAR').save()
Lugar(name = 'TECHINT').save()
Lugar(name = 'VIZCACHAS').save()