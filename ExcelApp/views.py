from django.shortcuts import render, redirect
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.contrib.staticfiles.storage import staticfiles_storage
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps
from ExcelApp.forms import ExcelForm
from ExcelApp.models import Excel, ProgramacionGeneral, Contratista, Transporte, ModalidadIngreso, TipoVehiculo, Carga, Destino, NumConvoy, Estado, Motivo, Conductor, Placa, ConductorArchivos, Observaciones, Categoria, PlacaArchivos, Lugar, FotosObservaciones

#importar liberia xlrd de excel
import datetime, xlrd
from datetime import time

#recoger el path donde estan los archivos excel
import Proyecto2
import os.path
from django.http import JsonResponse, HttpResponse
import json

#Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#subir un archivo al servidor
def create(request):  
    if not request.user.is_authenticated or request.user.role.id >= 3:
        return redirect("/")
    if request.method == 'POST':
        
        file = Excel.objects.last()
        if str(timezone.localtime(file.created_at))[0:10] == str(datetime.datetime.now())[:10]:    
            mensaje= "YA EXISTE UN ARCHIVO DEL DIA"
            return render(request,'e_new.html', {"mensaje": mensaje})

        data = request.POST
        files = request.FILES        
        e = Excel.objects.create(name = data['name'])          
        process_excel(files['file'], e.id)

        return redirect('/excel/index')
    
    return render(request,'e_new.html') 

def edit(request, id):  
    if not request.user.is_authenticated or request.user.role.id >= 3:
        return redirect("/")
    excel = Excel.objects.get(id=id)  
    return render(request,'e_edit.html', {'excel':excel})  

def update(request, id): 
    if not request.user.is_authenticated or request.user.role.id >= 3:
        return redirect("/") 
    excel = Excel.objects.filter(id=id).update(name = request.POST['name'])
    return redirect("/excel/index")      

def destroy(request, id):  
    if not request.user.is_authenticated or request.user.role.id >= 3:
        return redirect("/")
    excel = Excel.objects.get(id=id) 
    fecha = str(timezone.localtime(excel.created_at))
    fecha = fecha[:fecha.rfind(' ')]  
    excel.delete()  
    PlacaArchivos.objects.filter(date = fecha).delete()
    ConductorArchivos.objects.filter(date = fecha).delete()
    return redirect("/excel/index")

def index(request):  
    if not request.user.is_authenticated or request.user.role.id == 4 or request.user.role.id >= 6:
        return redirect("/")        
    
    if request.user.role.name == "Despachador" or request.user.role.name == "Desinfector":
        file = Excel.objects.last()
        if str(timezone.localtime(file.created_at))[0:10] == str(datetime.datetime.now())[:10]:    
            return render(request,"e_index.html", {'file': file})           
        return render(request,"e_index.html", {'file': None})
        
    files = Excel.objects.all().values('id', 'name', 'created_at').order_by('-created_at')        
    
    registros_paginator = 10
    page = request.GET.get('page', 1)

    paginator = Paginator(files, registros_paginator)
    try:
        files = paginator.page(page)
    except PageNotAnInteger:
        files = paginator.page(1)
    except EmptyPage:
        files = paginator.page(paginator.num_pages)
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

def db(request, id):
    if not request.user.is_authenticated or request.user.role.id == 4 or request.user.role.id >= 6:
        return redirect("/")
    form_datos = request.POST
    file = Excel.objects.get(id=id)
    tabla = ProgramacionGeneral.objects.filter(excel_id = id).order_by('id')
    unidades_despachadas = tabla.filter(estado_id = 1).count()
    unidades_canceladas = tabla.filter(estado_id = 2).count()
    unidades_desinfectadas = tabla.filter(cantidad_desinfectado__gte=1).count()
    transporte_ids = tabla.values_list('transporte', flat = True).distinct()
    contratista_ids = tabla.values_list('contratista', flat = True).distinct()
    conductor_ids = tabla.values_list('conductor', flat = True).distinct()
    num_convoy_ids = tabla.values_list('num_convoy', flat = True).distinct()
    placa_ids = tabla.values_list('conductor_placa', flat = True).distinct()
    registros_paginator = 10

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

        registros_paginator = tabla.count()

    transportes = Transporte.objects.filter(id__in = transporte_ids).order_by('name')
    contratistas = Contratista.objects.filter(id__in = contratista_ids).order_by('name')
    trabajadores = Conductor.objects.filter(id__in = conductor_ids).order_by('name')
    convoys = NumConvoy.objects.filter(id__in = num_convoy_ids).order_by('name')
    placas = Placa.objects.filter(id__in = placa_ids).order_by('placa1')
    lugares = Lugar.objects.all().order_by('name')
    
    fecha = str(timezone.localtime(file.created_at))
    fecha = fecha[:fecha.rfind(' ')]        
    conductor_archivos = ConductorArchivos.objects.filter(date = fecha) 
    vehiculo_archivos = PlacaArchivos.objects.filter(date = fecha)  

    page = request.GET.get('page', 1)

    paginator = Paginator(tabla, registros_paginator)
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
            "unidades_despachadas": unidades_despachadas,
            "unidades_canceladas": unidades_canceladas,
            "unidades_desinfectadas": unidades_desinfectadas,
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
    fecha = str(timezone.localtime(file.created_at))
    fecha = fecha[:fecha.rfind(' ')]  
    conductor_archivos = ConductorArchivos.objects.filter(date = fecha, conductor_id = id2)  
    conductor = Conductor.objects.get(id=id2)

    if conductor_archivos.exists(): 
        return render(request,'e_db_show_driver.html',{'conductor_archivos': conductor_archivos[0], 'conductor': conductor, 'fecha': fecha}) 

    return render(request,'e_db_show_driver.html', {'conductor': conductor, 'fecha': fecha}) 

def show_vehicle(request, id, id2, id3):    
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/")
    file = Excel.objects.get(id=id)
    fecha = str(timezone.localtime(file.created_at))
    fecha = fecha[:fecha.rfind(' ')]  
    vehiculo_archivos = PlacaArchivos.objects.filter(date = fecha, placa_id = id2) 
    vehiculo = Placa.objects.get(id=id2)
    desinfecciones = id3

    if vehiculo_archivos.exists(): 
        return render(request,'e_db_show_vehicle.html', {'vehiculo_archivos': vehiculo_archivos[0], 'vehiculo':vehiculo, 'fecha': fecha, 'desinfecciones': desinfecciones}) 

    return render(request,'e_db_show_vehicle.html', {'vehiculo':vehiculo, 'fecha': fecha, 'desinfecciones': desinfecciones}) 

def obs(request, id, id2): 
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/")    
    excel = Excel.objects.get(id=id)    
    fecha = str(timezone.localtime(excel.created_at))
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
    
    fotos = []
    contador = 0
    for obs in observaciones:
        fotos.append(FotosObservaciones.objects.filter(observacion_id = obs.id))
    
    return render(request,'e_db_obs.html',{'fila_programacion_general': fila_programacion_general, 'observaciones': observaciones, 'fotos': fotos,'existe': True, 'id_file': id, 'id_registro': id2, 'categorias': categorias, 'lugares': lugares}) 

def obs_destroy(request, id, id2, id3):  
    if not request.user.is_authenticated or request.user.role.id >= 3:
        return redirect("/")
    Observaciones.objects.filter(id = id3).delete()  
    obs = Observaciones.objects.filter(programacion_general_id = id2)
    if not obs: 
        fila_programacion_general = ProgramacionGeneral.objects.filter(id=id2)        
        fila_programacion_general.update(estado_id = 1)    
    return redirect("/excel/db/"+str(id)+"/obs/"+str(id2))

def obs_camera(request, id): 
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/")
    
    if request.method == 'POST':
        imagen_evidencia = "undefined"
        imagen_correctiva = "undefined"

        aux_primera_ie = "undefined"
        aux_primera_ic = "undefined"
        if len(request.POST['imagen_evidencia']) > 2:            
            imagen_evidencia = json.loads(request.POST['imagen_evidencia'])
        
        if len(request.POST['imagen_correctiva']) > 2:            
            imagen_correctiva = json.loads(request.POST['imagen_correctiva'])
        
        if imagen_evidencia == "undefined" or len(request.POST['descripcion']) == 0:
            return JsonResponse({"resultado": "fracaso"})     
        
        if imagen_evidencia != "undefined":
            imagen_evidencia[0] = "b'" + (imagen_evidencia[0])[22:] + "'" 
            aux_primera_ie = imagen_evidencia[0]
        
        if imagen_correctiva != "undefined":
            imagen_correctiva[0] = "b'" + (imagen_correctiva[0])[22:] + "'"    
            aux_primera_ic = imagen_correctiva[0]
       
        fecha = request.POST['fecha']
        fecha = fecha[:fecha.rfind('T')]         
        
        Observaciones(
            programacion_general_id_id = id, 
            descripcion = request.POST['descripcion'],
            accion_plan = request.POST['plan_accion'],
            evidencia_encode = aux_primera_ie,
            evidencia_correctiva_encode = aux_primera_ic,
            date = fecha,
            estado_id = 2,
            categoria_id = request.POST['categoria'],
            lugar_id = request.POST['lugar']
            ).save()

        fila_programacion_general = ProgramacionGeneral.objects.filter(id=id)
        fila_programacion_general.update(estado_id = 2)        

        vueltas_for = len(imagen_evidencia)
        min_vueltas = 1
        if imagen_correctiva != "undefined":
            vueltas_for = max(len(imagen_evidencia), len(imagen_correctiva))
            min_vueltas = min(len(imagen_evidencia), len(imagen_correctiva))
        else:
            imagen_correctiva = ""
        if vueltas_for >= 2:
            ultima_observacion = Observaciones.objects.last()
            for i in range(1, vueltas_for):
                if len(imagen_evidencia) == len(imagen_correctiva): 
                    FotosObservaciones(
                        observacion_id = ultima_observacion.id,                       
                        evidencia_encode = "b'" + (imagen_evidencia[i])[22:] + "'",
                        evidencia_correctiva_encode = "b'" + (imagen_correctiva[i])[22:] + "'",                       
                    ).save()

                if len(imagen_evidencia) > len(imagen_correctiva):                    
                    if(min_vueltas <= i):
                        FotosObservaciones(
                            observacion_id = ultima_observacion.id,                         
                            evidencia_encode = "b'" + (imagen_evidencia[i])[22:] + "'",
                            evidencia_correctiva_encode = "undefined",                       
                        ).save()
                    else:
                        FotosObservaciones(
                            observacion_id = ultima_observacion.id,                         
                            evidencia_encode = "b'" + (imagen_evidencia[i])[22:] + "'",
                            evidencia_correctiva_encode = "b'" + (imagen_correctiva[i])[22:] + "'",                       
                        ).save()
                        
                if len(imagen_correctiva) > len(imagen_evidencia):                    
                    if(min_vueltas <= i):
                        FotosObservaciones(
                            observacion_id = ultima_observacion.id,                         
                            evidencia_encode = "undefined",
                            evidencia_correctiva_encode = "b'" + (imagen_correctiva[i])[22:],                       
                        ).save()
                    else:
                        FotosObservaciones(
                            observacion_id = ultima_observacion.id,                         
                            evidencia_encode = "b'" + (imagen_evidencia[i])[22:] + "'",
                            evidencia_correctiva_encode = "b'" + (imagen_correctiva[i])[22:] + "'",                       
                        ).save()
                    
            return JsonResponse({"resultado": "insertar" + str(vueltas_for)})     

        return JsonResponse({"resultado": "exito"}) 

def obs_update(request, id, id2, id3): 
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/")
    excel = Excel.objects.get(id=id)    
    fecha = str(timezone.localtime(excel.created_at))
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

def image_editor(request, id, id2):
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/")    
    if request.method == 'POST': 
        imagen = request.POST['imagen']
        imagen = "b'" + imagen[22:] + "'"

        if(id2 == 0):
            observacion_registro = Observaciones.objects.filter(id = id)
            obs_tipo = request.POST['observacion_tipo']
            
            if obs_tipo == "evidencia":
                observacion_registro.update(evidencia_encode = imagen)

            if obs_tipo == "evidencia_correctiva":
                observacion_registro.update(evidencia_correctiva_encode = imagen)
        else:
            fotos_observacion = FotosObservaciones.objects.filter(id = id2)
            obs_tipo = request.POST['observacion_tipo']
            
            if obs_tipo == "evidencia":
                fotos_observacion.update(evidencia_encode = imagen)

            if obs_tipo == "evidencia_correctiva":
                fotos_observacion.update(evidencia_correctiva_encode = imagen)

        return JsonResponse({"resultado": "ok"})        

#actualizar evidencia correctiva con la camara
def update_image_editor(request, id):
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/")    
    if request.method == 'POST': 
        imagen = request.POST['data']
        imagen = "b'" + imagen[22:] + "'"

        observacion_registro = Observaciones.objects.get(id = id)

        if observacion_registro.evidencia_correctiva_encode == "undefined":        
            observacion_registro.evidencia_correctiva_encode = imagen
            observacion_registro.save()
            return JsonResponse({"resultado": "ok"})

        fo = FotosObservaciones.objects.filter(observacion_id = observacion_registro.id, evidencia_correctiva_encode="undefined")
        if fo:            
            fo[0].evidencia_correctiva_encode = imagen
            fo[0].save()
        else:
            FotosObservaciones(
                observacion_id = observacion_registro.id,                         
                evidencia_encode = "undefined",
                evidencia_correctiva_encode = imagen
            ).save()            
                
        return JsonResponse({"resultado": "ok"})

def take_photo_vehicle(request, id):
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/")    
    if request.method == 'POST': 
        imagen = request.POST['imagen']
        imagen = "b'" + imagen[22:] + "'"

        num_foto = request.POST['num_foto']
        fecha = request.POST['fecha']

        PlacaArchivos.objects.get_or_create(date = fecha, placa_id = id)  

        if num_foto == "foto1":
            PlacaArchivos.objects.filter(date = fecha, placa_id = id).update(photo1_encode = imagen)
        if num_foto == "foto2":
            PlacaArchivos.objects.filter(date = fecha, placa_id = id).update(photo2_encode = imagen)
        if num_foto == "foto3":
            PlacaArchivos.objects.filter(date = fecha, placa_id = id).update(photo3_encode = imagen)
        if num_foto == "foto4":
            PlacaArchivos.objects.filter(date = fecha, placa_id = id).update(photo4_encode = imagen)

        return JsonResponse({"resultado": "ok"}) 
        
import zipfile 
from wsgiref.util import FileWrapper
def download_photos_v(request, id):
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/")    

    #fecha son los primeros 10 caracteres, id los restantes
    pa = PlacaArchivos.objects.get(placa_id = id[10:],date = id[:10])
    name = pa.placa.placa1+'_'+pa.placa.placa2+'_'+id[:10]+'.zip'

    hay_fotos = 0
    foto1 = pa.photo1_encode
    foto2 = pa.photo2_encode
    foto3 = pa.photo3_encode
    foto4 = pa.photo4_encode
    checklist = pa.checklist_file_encode
    
    if foto1 != None and foto1 != "undefined":
        foto1 = foto1[2:-1]    
        im = Image.open(BytesIO(base64.b64decode(foto1))) 
        im.save('foto1.png', 'PNG')
        hay_fotos = 1
    if foto2 != None and foto2 != "undefined":
        foto2 = foto2[2:-1]    
        im = Image.open(BytesIO(base64.b64decode(foto2))) 
        im.save('foto2.png', 'PNG')
        hay_fotos = 1
    if foto3 != None and foto3 != "undefined":
        foto3 = foto3[2:-1]    
        im = Image.open(BytesIO(base64.b64decode(foto3))) 
        im.save('foto3.png', 'PNG')
        hay_fotos = 1
    if foto4 != None and foto4 != "undefined":
        foto4 = foto4[2:-1]    
        im = Image.open(BytesIO(base64.b64decode(foto4))) 
        im.save('foto4.png', 'PNG')
        hay_fotos = 1
    if checklist != None and checklist != "undefined":
        checklist = checklist[2:-1]    
        im = Image.open(BytesIO(base64.b64decode(checklist))) 
        im.save('checklist.png', 'PNG')
        hay_fotos = 1
    
    if hay_fotos == 1:
        with zipfile.ZipFile(name, 'w') as export_zip:        
            if foto1 != None and foto1 != "undefined":
                export_zip.write("foto1.png")
            if foto2 != None and foto2 != "undefined":
                export_zip.write("foto2.png")
            if foto3 != None and foto3 != "undefined":
                export_zip.write("foto3.png")
            if foto4 != None and foto4 != "undefined":
                export_zip.write("foto4.png")
            if checklist != None and checklist != "undefined":
                export_zip.write("checklist.png")
        wrapper = FileWrapper(open(name, 'rb'))
        content_type = 'application/zip'
        content_disposition = 'attachment; filename='+name

        response = HttpResponse(wrapper, content_type=content_type)
        response['Content-Disposition'] = content_disposition 
        return response
        
    return HttpResponse('')

def download_photos_c(request, id):
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/")    

    #fecha son los primeros 10 caracteres, id los restantes
    conductor = ConductorArchivos.objects.get(conductor_id = id[10:],date = id[:10])
    name = conductor.conductor.name+'_'+id[:10]+'.zip'

    hay_fotos = 0
    declaracion = conductor.declaracion_file_encode
    fatiga = conductor.fatiga_file_encode
    iperc = conductor.iperc_file_encode
    
    if declaracion != None and declaracion != "undefined":
        declaracion = declaracion[2:-1]    
        im = Image.open(BytesIO(base64.b64decode(declaracion))) 
        im.save('declaracion.png', 'PNG')
        hay_fotos = 1
    if fatiga != None and fatiga != "undefined":
        fatiga = fatiga[2:-1]    
        im = Image.open(BytesIO(base64.b64decode(fatiga))) 
        im.save('fatiga.png', 'PNG')
        hay_fotos = 1
    if iperc != None and iperc != "undefined":
        iperc = iperc[2:-1]    
        im = Image.open(BytesIO(base64.b64decode(iperc))) 
        im.save('iperc.png', 'PNG')
        hay_fotos = 1
    
    if hay_fotos == 1:
        with zipfile.ZipFile(name, 'w') as export_zip:        
            if declaracion != None and declaracion != "undefined":
                export_zip.write("declaracion.png")
            if fatiga != None and fatiga != "undefined":
                export_zip.write("fatiga.png")
            if iperc != None and iperc != "undefined":
                export_zip.write("iperc.png")

        wrapper = FileWrapper(open(name, 'rb'))
        content_type = 'application/zip'
        content_disposition = 'attachment; filename='+name

        response = HttpResponse(wrapper, content_type=content_type)
        response['Content-Disposition'] = content_disposition 
        return response
        
    return HttpResponse('')

def add_disinfect(request):
    if not request.user.is_authenticated or request.user.role.id == 4 or request.user.role.id >= 6:
        return redirect("/")    
    if request.method == 'POST': 
        file_id = request.POST['file_id']
        conductor_placa_id = request.POST['conductor_placa_id']
        comentario = request.POST['comentario']

        results = ProgramacionGeneral.objects.filter(excel_id = file_id, conductor_placa_id = conductor_placa_id)  
        for result in results:
            if result.cantidad_desinfectado is None:
                result.cantidad_desinfectado = 1
                result.comentario = comentario
                result.save()
            else:
                result.cantidad_desinfectado += 1
                result.comentario = comentario
                result.save()
        return JsonResponse({"resultado": "ok"}) 
################################################### metodos privados##############################

#metodo para insertar una observacion en cualquier modal
def __obs_modales(request, id, id2, tipo_archivo, categoria, pertenece_a):   
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/")
    data = request.POST   
    fecha = str(data['fecha'])    
    fecha = fecha[:fecha.rfind('T')]
    uploaded_file = request.POST['file']     
    uploaded_file_obs = request.POST['file_obs']
    uploaded_file_corrected = request.POST['file_lev']    

    #Solo para el archivo fatiga, declaracion jurada e iperc, independiente de la observacion
    if pertenece_a == "conductor":      
        if uploaded_file != "undefined":
            uploaded_file = "b'" + uploaded_file[22:] + "'"
            imagen_watermark = __water_mark_function(request, fecha, uploaded_file)
            ConductorArchivos.objects.get_or_create(date = fecha, conductor_id = id)    
            if tipo_archivo == "fatigas":
                ConductorArchivos.objects.filter(date = fecha, conductor_id = id).update(fatiga_file_encode = imagen_watermark)
            if tipo_archivo == "declaracion":
                ConductorArchivos.objects.filter(date = fecha, conductor_id = id).update(declaracion_file_encode = imagen_watermark)
            if tipo_archivo == "iperc":
                ConductorArchivos.objects.filter(date = fecha, conductor_id = id).update(iperc_file_encode = imagen_watermark)
            return JsonResponse({"resultado": "ok conductor"})
    
    #solo para checklist
    if pertenece_a == "vehiculo":              
        if uploaded_file != "undefined":
            uploaded_file = "b'" + uploaded_file[22:] + "'"
            PlacaArchivos.objects.get_or_create(date = fecha, placa_id = id)  
            if tipo_archivo == "checklist":                   
                imagen_watermark = __water_mark_function(request, fecha, uploaded_file)
                PlacaArchivos.objects.filter(date = fecha, placa_id = id).update(checklist_file_encode = imagen_watermark)
            return JsonResponse({"resultado": "ok checklist"})
        
    #ver si existe una observacion a ser insertada en base a la imagen o a la descripcion ingresada    
    if uploaded_file_obs != "undefined" or data['id_mod_des']:         
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

        if uploaded_file_obs != "undefined" :            
            name = "b'" + uploaded_file_obs[22:] + "'"

        if uploaded_file_corrected != "undefined":
            name_corrected = "b'" + uploaded_file_corrected[22:] + "'"
                
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

def __water_mark_function(request, fecha, uploaded_file):  
    
    #cargar template de la marca de agua           
    url = staticfiles_storage.path('img/water_mark.png')
    personal_water_mark = Image.open(url)
    draw = ImageDraw.Draw(personal_water_mark)
    #dibujar datos que iran
    font = ImageFont.truetype(staticfiles_storage.path('fonts/Roboto/Roboto-Bold.ttf'), size=45)
    (x, y) = (180, 350)
    nombre_usuario = request.user.username
    color = 'rgb(0, 0, 0)' # black color
    draw.text((x, y), nombre_usuario, fill=color, font=font)

    font = ImageFont.truetype(staticfiles_storage.path('fonts/Roboto/Roboto-Bold.ttf'), size=35)
    (x, y) = (320, 400)
    empresa = 'SCANGLOBAL'
    color = 'rgb(255, 0, 0)' # red color
    draw.text((x, y), empresa, fill=color, font=font)

    (x, y) = (330, 440)
    color = 'rgb(0, 0, 0)' # black color
    draw.text((x, y), fecha, fill=color, font=font)
            
    data = uploaded_file[2:-1]
    im = Image.open(BytesIO(base64.b64decode(data)))    
    size = 1366, 768
    im.thumbnail(size, Image.ANTIALIAS)
    im = im.resize(size, Image.ANTIALIAS) 

    #rotar por si esta horizontal
    base_image = ImageOps.exif_transpose(im)
    
    #obtener dimensiones de la imagen subida
    width, height = base_image.size
    
    #ubicar siempre abajo izquierda la marca de agua
    position = (width - 384 , height - 384)
    #disminuir el tamanio de la marca de agua
    size = 384, 384
    personal_water_mark.thumbnail(size, Image.ANTIALIAS)
    #poner marca de agua
    base_image.paste(personal_water_mark, position, mask=personal_water_mark)
    #base_image.save('greeting_card.png')#solo para verificar

    #abrir un buffer para base64
    buf = BytesIO()
    base_image.save(buf, 'png', optimize=True, quality=90)                
    buf.seek(0)
    #codificar base 64
    imagen_base64 = __encode64(buf)
    buf.close()
    
    return imagen_base64
    
	  