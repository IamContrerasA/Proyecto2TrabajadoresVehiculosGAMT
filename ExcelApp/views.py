from django.shortcuts import render, redirect

from django.core.files.storage import FileSystemStorage
from django.conf import settings
from ExcelApp.forms import ExcelForm
from ExcelApp.models import Excel, ProgramacionGeneral, Contratista, Transporte, ModalidadIngreso, TipoVehiculo, Carga, Destino, NumConvoy, Estado, Motivo, Conductor, Placa, ConductorArchivos, Observaciones, Categoria, PlacaArchivos, Lugar

#importar liberia xlrd de excel
import datetime, xlrd
from datetime import time

#recoger el path donde estan los archivos excel
import Proyecto2
import os.path
from django.http import JsonResponse, HttpResponse

#subir un archivo al servidor
def create(request):  
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/")
    if request.method == 'POST':
        data = request.POST
        files = request.FILES
        #form = ExcelForm(request.POST, request.FILES)
        #if form.is_valid():
        #    file = form.save()  

        e = Excel.objects.create(name = data['name'])          
        process_excel(files['file'], e.id)

        return redirect('/excel/index')
    
    return render(request,'e_new.html') 

def index(request):  
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/")
    files = Excel.objects.all().values('id', 'name', 'created_at')
    return render(request,"e_index.html", {'files': files}) 

#Procesar el excel
def process_excel(excel, id):  
        
    wb = xlrd.open_workbook(filename=None, file_contents=excel.read())
    sheet = wb.sheet_by_index(0)     
    
    #ver en que fila comenzar a leer
    row_start = ''
    for i in range (0, sheet.nrows):
        if(sheet.cell_value(i, 0).upper() == 'EA'):
            row_start = i
            break      
    # print(str(sheet.cell_value(20, 8)))
    # print(str(sheet.cell_value(26, 8)))
    # print(str(sheet.cell_value(41, 8)))
    for i in range(row_start + 1, sheet.nrows):     
        db_register = []
        for j in range(sheet.ncols): 
            value = sheet.cell_value(i, j)
            db = value

            if value == "x" or value == "X" or value == "-" or value == "N.A" or value == "N.A." or value == "N/A":
                value = ""
                db = value

            if j == 8 and value != "DNI":
                value = str(value)
                pos = value.rfind(".0")
                if pos != -1:
                    value = value[:pos]                    
                    db = value
    
            if j == 14 and value != "TELÉFONO ESCOLTA":
                value = str(value)
                pos = value.rfind(".0")
                if pos != -1:
                    value = value[:pos]                    
                    db = value

            if j == 15 and value != "TELÉFONO SATELITAL":
                value = str(value)
                pos = value.rfind(".0")
                if pos != -1:
                    value = value[:pos]                    
                    db = value
            
            if j == 22 and value != "FECHA DE LLEGADA A CHECKPOINT":                
                if value != "":
                    value = datetime.datetime(*xlrd.xldate_as_tuple(value, wb.datemode))
                    value = str(value)[0:10]
                    db = value
                  
            if j == 23 and value != "HORA DE LLEGADA A CHECKPOINT":                
                if value != "":                    
                    date_values = xlrd.xldate_as_tuple(value, wb.datemode)
                    time_value = time(*date_values[2:])                    
                    value = str(time_value)[3:]
                    db = value

            if j == 24 and i >= row_start + 2: 
                
                if value != "" and type(value) != str :                         
                    date_values = xlrd.xldate_as_tuple(value, wb.datemode)  
                    time_value = time(*date_values[2:])                    
                    value = str(time_value)[3:]
                    db = value            

            if j == 26 and value != "ETA SITE":                
                if value != "":
                    value = datetime.datetime(*xlrd.xldate_as_tuple(value, wb.datemode))                      
                    value = str(value)[0:10]
                    db = value            
            
            db_register.append(db)
            
        if i >= row_start + 2 :
            insertDataBase(db_register, id)        

    return JsonResponse({"resultado": "ok"})    

def insertDataBase(row, id):     
    contratista = Contratista.objects.get_or_create(name = str(row[1]).strip())
    transporte = Transporte.objects.get_or_create(name = str(row[2]).strip())
    modalidad_ingreso = ModalidadIngreso.objects.get_or_create(name = str(row[3]).strip())
    tipo_vehiculo = TipoVehiculo.objects.get_or_create(name = str(row[4]).strip())
    conductor_placa = Placa.objects.get_or_create(placa1 = str(row[5]).strip(), placa2 = str(row[6]).strip())
    conductor = Conductor.objects.get_or_create(name = str(row[7]).strip(), dni = str(row[8]).strip(), license = str(row[9]).strip())    
    count_conductor = Conductor.objects.filter(name = str(row[10]).strip(), license = str(row[11]).strip())    
    if count_conductor.count() == 0:
        conductor_relevo = Conductor.objects.get_or_create(name = str(row[10]).strip(), license = str(row[11]).strip())
    else:
        conductor_relevo = count_conductor
    conductor_relevo_placa = Placa.objects.get_or_create(placa1 = str(row[12]).strip(), placa2 = str(row[13]).strip())
    carga = Carga.objects.get_or_create(name = str(row[17]).strip())
    desde = Destino.objects.get_or_create(name = str(row[20]).strip())
    hacia = Destino.objects.get_or_create(name = str(row[21]).strip())
    num_convoy = NumConvoy.objects.get_or_create(name = str(row[25]).strip())
    estado = Estado.objects.get_or_create(name = str(row[27]).strip())
    motivo = Motivo.objects.get_or_create(name = str(row[28]).strip())    
    
    ProgramacionGeneral(
        ea=row[0], 
        excel_id = id, 
        contratista = contratista[0], 
        transporte = transporte[0], 
        modalidad_ingreso = modalidad_ingreso[0],
        tipo_vehiculo = tipo_vehiculo[0],
        conductor_placa = conductor_placa[0],
        conductor = conductor[0],
        conductor_relevo = conductor_relevo[0],        
        conductor_relevo_placa = conductor_relevo_placa[0],
        telefono_escolta = row[14],
        telefono_satelital = row[15],
        pasajeros = row[16],
        carga = carga[0],
        num_guia = row[18],
        descripcion = row[19],
        desde = desde[0],
        hacia = hacia[0],
        fecha_llegada = row[22],
        hora_llegada = row[23],
        hora_partida = row[24],
        num_convoy = num_convoy[0],
        eta_site = row[26],
        estado = estado[0],
        motivo = motivo[0]
        ).save()    


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def db(request, id):
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/")
    form_datos = request.POST
    file = Excel.objects.get(id=id)
    tabla = ProgramacionGeneral.objects.filter(excel_id = id).order_by('id')
    transporte_ids = tabla.values_list('transporte', flat = True).distinct()
    contratista_ids = tabla.values_list('contratista', flat = True).distinct()
    conductor_ids = tabla.values_list('conductor', flat = True).distinct()
    num_convoy_ids = tabla.values_list('num_convoy', flat = True).distinct()
    placa_ids = tabla.values_list('conductor_placa', flat = True).distinct()

    if request.method == 'POST':         

        f_transporte = int(form_datos['transporte'])
        f_contratista = int(form_datos['contratista'])
        f_conductor = int(form_datos['conductor'])
        f_num_convoy = int(form_datos['num_convoy'])
        f_placa = int(form_datos['placa'])

        if f_transporte > -1 and f_contratista > -1 and f_conductor > -1 and f_num_convoy > -1 and f_placa > -1:
            tabla = ProgramacionGeneral.objects.filter(excel_id = id, transporte = f_transporte, contratista = f_contratista, conductor = f_conductor, num_convoy=f_num_convoy, conductor_placa = f_placa).order_by('id')

        elif f_transporte > -1 and f_contratista > -1 and f_conductor > -1 and f_num_convoy > -1 :
            tabla = ProgramacionGeneral.objects.filter(excel_id = id, transporte = f_transporte, contratista = f_contratista, conductor = f_conductor, num_convoy=f_num_convoy).order_by('id')

        elif f_transporte > -1 and f_contratista > -1 and f_conductor > -1 :
            tabla = ProgramacionGeneral.objects.filter(excel_id = id, transporte = f_transporte, contratista = f_contratista, conductor = f_conductor).order_by('id')

        elif f_transporte > -1 and f_contratista > -1 :
            tabla = ProgramacionGeneral.objects.filter(excel_id = id, transporte = f_transporte, contratista = f_contratista).order_by('id')

        elif f_transporte > -1 :
            transporte_ids = tabla.values_list('transporte', flat = True).distinct()
            tabla = ProgramacionGeneral.objects.filter(excel_id = id, transporte = f_transporte).order_by('id')
 
        elif f_contratista > -1 :
            contratista_ids = tabla.values_list('contratista', flat = True).distinct()
            tabla = ProgramacionGeneral.objects.filter(excel_id = id, contratista = f_contratista).order_by('id')
        
        elif f_conductor > -1 :
            conductor_ids = tabla.values_list('conductor', flat = True).distinct()
            tabla = ProgramacionGeneral.objects.filter(excel_id = id, conductor = f_conductor).order_by('id')

        elif f_num_convoy > -1 :
            num_convoy_ids = tabla.values_list('num_convoy', flat = True).distinct()
            tabla = ProgramacionGeneral.objects.filter(excel_id = id, num_convoy = f_num_convoy).order_by('id')

        elif f_placa > -1 :
            placa_ids = tabla.values_list('conductor_placa', flat = True).distinct()
            tabla = ProgramacionGeneral.objects.filter(excel_id = id, conductor_placa = f_placa).order_by('id')        
        
    transportes = Transporte.objects.filter(id__in = transporte_ids).order_by('name')
    contratistas = Contratista.objects.filter(id__in = contratista_ids).order_by('name')
    trabajadores = Conductor.objects.filter(id__in = conductor_ids).order_by('name')
    convoys = NumConvoy.objects.filter(id__in = num_convoy_ids).order_by('name')
    placas = Placa.objects.filter(id__in = placa_ids).order_by('placa1')
    lugares = Lugar.objects.all().order_by('name')

    fecha = str(file.created_at)
    fecha = fecha[:fecha.rfind(' ')]        
    conductor_archivos = ConductorArchivos.objects.filter(date = fecha) 
    vehiculo_archivos = PlacaArchivos.objects.filter(date = fecha)  

    page = request.GET.get('page', 1)

    paginator = Paginator(tabla, 10)
    try:
        tabla = paginator.page(page)
    except PageNotAnInteger:
        tabla = paginator.page(1)
    except EmptyPage:
        tabla = paginator.page(paginator.num_pages)


    return render(
        request,
        "e_db.html", 
        {
            "file": file, 
            "tabla": tabla, 
            "transportes": transportes, 
            "contratistas": contratistas,
            "trabajadores": trabajadores,
            "convoys": convoys,
            "placas": placas,
            "datos": form_datos,
            "conductor_archivos": conductor_archivos,
            "vehiculo_archivos": vehiculo_archivos,
            "lugares": lugares
        }) 

def fatiga_modal(request, id, id2):
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/")
    if request.method == 'POST':  
        return __obs_modales(request, id, id2, "fatigas", "DOCUMENTACION", "conductor")        

def declaracion_modal(request, id, id2):
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/")
    if request.method == 'POST':  
        return __obs_modales(request, id, id2, "declaracion", "DOCUMENTACION", "conductor") 

def iperc_modal(request, id, id2):
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/")
    if request.method == 'POST':  
        return __obs_modales(request, id, id2, "iperc", "DOCUMENTACION", "conductor") 

def checklist_modal(request, id, id2):
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/")
    if request.method == 'POST':  
        return __obs_modales(request, id, id2, "checklist", "DOCUMENTACION", "vehiculo") 

def show_driver(request, id, id2):    
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/")
    file = Excel.objects.get(id=id)
    fecha = str(file.created_at)
    fecha = fecha[:fecha.rfind(' ')]  
    conductor_archivos = ConductorArchivos.objects.filter(date = fecha, conductor_id = id2)  

    if conductor_archivos.exists(): 
        return render(request,'e_db_show_driver.html',{'conductor_archivos': conductor_archivos[0]}) 

    return render(request,'e_db_show_driver.html') 

def show_vehicle(request, id, id2):    
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/")
    file = Excel.objects.get(id=id)
    fecha = str(file.created_at)
    fecha = fecha[:fecha.rfind(' ')]  
    vehiculo_archivos = PlacaArchivos.objects.filter(date = fecha, placa_id = id2) 

    if vehiculo_archivos.exists(): 
        return render(request,'e_db_show_vehicle.html',{'vehiculo_archivos': vehiculo_archivos[0]}) 

    return render(request,'e_db_show_vehicle.html') 

def obs(request, id, id2): 
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/")    
    excel = Excel.objects.get(id=id)
    fecha = str(excel.created_at)
    fecha = fecha[:fecha.rfind(' ')]  

    observaciones = Observaciones.objects.filter(programacion_general_id = id2, date = fecha)  
    fila_programacion_general = ProgramacionGeneral.objects.filter(id=id2) 
    estado_desaprobado = Estado.objects.get(name = "DESAPROBADO")
    categorias = Categoria.objects.all()
    lugares = Lugar.objects.all()

    if request.method == 'POST':                  
        data = request.POST 
        name = "undefined"
        name_corrected = "undefined"      
        uploaded_file = request.FILES['evidencia'] if 'evidencia' in request.FILES else False
        uploaded_file_corrected = request.FILES['levantamiento'] if 'levantamiento' in request.FILES else False        
        categoria = Categoria.objects.get(id = data['categoria'])
        lugar = Lugar.objects.get(id = data['lugar'])

        last_id = Observaciones.objects.last()
        if last_id:
            last_id = str(last_id.id + 1)
        else:
            last_id = "1"

        if uploaded_file :                        
            name = __encode64(uploaded_file)            

        if uploaded_file_corrected :                        
            name_corrected = __encode64(uploaded_file_corrected)            

        Observaciones(
            programacion_general_id = fila_programacion_general[0], 
            descripcion = data['descripcion'],  
            accion_plan = data['plan_accion'], 
            evidencia_encode = name,
            evidencia_correctiva_encode = name_corrected,
            date = fecha, 
            estado_id = estado_desaprobado.id,
            categoria = categoria,
            lugar = lugar
            ).save()  
        
        fila_programacion_general.update(estado_id = estado_desaprobado.id)

        return redirect('/excel/db/'+str(id)+'/obs/'+str(id2))   

    if not observaciones.exists():         
        return render(request,'e_db_obs.html',{'fila_programacion_general': fila_programacion_general, 'existe': False, 'id_file': id, 'id_registro': id2, 'categorias': categorias, 'lugares': lugares}) 
    
    return render(request,'e_db_obs.html',{'fila_programacion_general': fila_programacion_general, 'observaciones': observaciones, 'existe': True, 'id_file': id, 'id_registro': id2, 'categorias': categorias, 'lugares': lugares}) 

def obs_camera(request, id): 
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/")
    
    if request.method == 'POST':         
        
        imagen_evidencia = request.POST['imagen_evidencia']
        if imagen_evidencia == "undefined" or len(request.POST['descripcion']) == 0:
            return JsonResponse({"resultado": "fracaso"})

        if imagen_evidencia != "undefined":
            imagen_evidencia = "b'" + imagen_evidencia[22:] + "'" 

        imagen_correctiva = request.POST['imagen_correctiva']  
        if imagen_correctiva != "undefined":
            imagen_correctiva = "b'" + imagen_correctiva[22:] + "'"    
        
        Observaciones(
            programacion_general_id_id = id, 
            descripcion = request.POST['descripcion'],
            accion_plan = request.POST['plan_accion'],
            evidencia_encode = imagen_evidencia,
            evidencia_correctiva_encode = imagen_correctiva,
            date = "2020-12-07",
            estado_id = 2,
            categoria_id = request.POST['categoria'],
            lugar_id = request.POST['lugar']
            ).save() 
        
        return JsonResponse({"resultado": "exito"}) 

def obs_update(request, id, id2, id3): 
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/")
    excel = Excel.objects.get(id=id)
    fecha = str(excel.created_at)
    fecha = fecha[:fecha.rfind(' ')] 

    if request.method == 'POST':    
        data = request.POST        
        name = "undefined"
        name_corrected = "undefined"
        uploaded_file = request.FILES['file'] if 'file' in request.FILES else False
        uploaded_file_corrected = request.FILES['file_id_levantamiento_'] if 'file_id_levantamiento_' in request.FILES else False       
        categoria = Categoria.objects.get(id = data['categoria'])
        lugar = Lugar.objects.get(id = data['lugar'])

        if uploaded_file :  
            name = __encode64(uploaded_file)

        if uploaded_file_corrected :
            name_corrected = __encode64(uploaded_file_corrected)
        
        observacion_registro = Observaciones.objects.filter(id = id3)

        if name == "undefined" and observacion_registro[0].evidencia_encode:
            name = observacion_registro[0].evidencia_encode

        if name_corrected == "undefined" and observacion_registro[0].evidencia_correctiva_encode:
            name_corrected = observacion_registro[0].evidencia_correctiva_encode

        observacion_registro.update(
            descripcion = data['descripcion'],  
            evidencia_encode = name,
            evidencia_correctiva_encode = name_corrected,
            accion_plan = data['plan_accion'],
            categoria = categoria,
            lugar = lugar
        )       

        return JsonResponse({"resultado": "exito"})  

def obs_aprove(request, id, id2, id3):
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/")
    Observaciones.objects.filter(id=id3).update(estado = 1)  
    #Si todas las observaciones estan aprobadas, actualizar programacion general
    pg = Observaciones.objects.filter(programacion_general_id = id2)
    
    aprobar_registro = True
    for row in pg:
        
        if row.estado.id == 2:
            aprobar_registro = False

    if aprobar_registro:        
        ProgramacionGeneral.objects.filter(id=id2).update(estado = 1)
    
    return redirect("/excel/db/"+str(id)+"/obs/"+str(id2)) 

def obs_disaprove(request, id, id2, id3): 
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/")
    Observaciones.objects.filter(id=id3).update(estado = 2)      
    ProgramacionGeneral.objects.filter(id=id2).update(estado = 2)
    return redirect("/excel/db/"+str(id)+"/obs/"+str(id2)) 

def image_editor(request, id):
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/")    
    if request.method == 'POST': 
        imagen = request.POST['imagen']
        observacion_registro = Observaciones.objects.filter(id = id)
        obs_tipo = request.POST['observacion_tipo']

        imagen = "b'" + imagen[22:] + "'"
        
        if obs_tipo == "evidencia":
            observacion_registro.update(evidencia_encode = imagen)

        if obs_tipo == "evidencia_correctiva":
            observacion_registro.update(evidencia_correctiva_encode = imagen)

        return JsonResponse({"resultado": "ok"})        
        
################################################### metodos privados##############################

#metodo para insertar una observacion en cualquier modal
def __obs_modales(request, id, id2, tipo_archivo, categoria, pertenece_a):   
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/")
    data = request.POST   
    fecha = str(data['fecha'])
    fecha = fecha[:fecha.rfind('T')]
    uploaded_file = request.FILES['file'] if 'file' in request.FILES else False
    uploaded_file_obs = request.FILES['file_obs'] if 'file_obs' in request.FILES else False
    uploaded_file_corrected = request.FILES['file_lev'] if 'file_lev' in request.FILES else False 
    
    #Solo para el archivo fatiga, declaracion jurada e iperc, independiente de la observacion
    if pertenece_a == "conductor":              
        if uploaded_file:              
            name = __encode64(uploaded_file)

            ConductorArchivos.objects.get_or_create(date = fecha, conductor_id = id)  
            if tipo_archivo == "fatigas":
                ConductorArchivos.objects.filter(date = fecha, conductor_id = id).update(fatiga_file_encode = name)
            if tipo_archivo == "declaracion":
                ConductorArchivos.objects.filter(date = fecha, conductor_id = id).update(declaracion_file_encode = name)
            if tipo_archivo == "iperc":
                ConductorArchivos.objects.filter(date = fecha, conductor_id = id).update(iperc_file_encode = name)
            return JsonResponse({"resultado": "ok conductor"})
    
    #solo para checklist
    if pertenece_a == "vehiculo":              
        if uploaded_file:
            name = __encode64(uploaded_file)

            PlacaArchivos.objects.get_or_create(date = fecha, placa_id = id)  
            if tipo_archivo == "checklist":
                PlacaArchivos.objects.filter(date = fecha, placa_id = id).update(checklist_file_encode = name)
            return JsonResponse({"resultado": "ok checklist"})
    
    #ver si existe una observacion a ser insertada en base a la imagen o a la descripcion ingresada    
    if uploaded_file_obs or data['id_mod_des']:         
        fila_programacion_general = ProgramacionGeneral.objects.filter(id=id2) 
        estado_desaprobado = Estado.objects.get(name = "DESAPROBADO")
        categoria = Categoria.objects.get(name = categoria)
        name = "undefined"
        name_corrected = "undefined"
        last_id = Observaciones.objects.last()
        if last_id:
            last_id = str(last_id.id + 1)
        else:
            last_id = "1"

        if uploaded_file_obs :
            name = __encode64(uploaded_file_obs)

        if uploaded_file_corrected :
            name_corrected = __encode64(uploaded_file_corrected)
                
        Observaciones(
            programacion_general_id = fila_programacion_general[0], 
            descripcion = data['id_mod_des'],  
            accion_plan = data['id_plan_accion'], 
            evidencia_encode = name,
            evidencia_correctiva_encode = name_corrected,
            date = fecha, 
            estado_id = estado_desaprobado.id,
            categoria = categoria,
            lugar_id = int(data['lugar'])
            ).save()  
        
        fila_programacion_general.update(estado_id = estado_desaprobado.id)
        return JsonResponse({"resultado": "ok"})

    else:  
        return JsonResponse({"resultado": "no guardo nada"})

import base64
def __encode64(photo):  
   
  enc =  base64.b64encode(photo.read())
  
  return enc