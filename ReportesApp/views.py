from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from ExcelApp.models import Observaciones, Lugar, Contratista, Categoria, FotosObservaciones
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.core import serializers

def index(request):
  if not request.user.is_authenticated or request.user.role.id >= 4:
    return redirect("/")
  contratistas = Contratista.objects.all()
  lugares = Lugar.objects.all()
  categorias = Categoria.objects.all()
  return render(request,"r_index.html", {"lugares": lugares, "contratistas": contratistas, "categorias": categorias})  

def create(request): 
  if not request.user.is_authenticated or request.user.role.id >= 4:
    return redirect("/")   
  observaciones = []  
  if request.method == 'POST':
    data = request.POST
    print (data)
    contratista_id = int(data['contratista'])
    lugar_id = int(data['lugar'])
    categoria_id = int(data['categoria'])

    if contratista_id != -1 and lugar_id != -1 and categoria_id != -1:
      observaciones = Observaciones.objects.filter(
        date__range = [data['start_date'],data['end_date']],
        programacion_general_id__contratista__id = contratista_id,
        lugar_id = lugar_id,
        categoria_id = categoria_id
        ).values(
          'id',
          'categoria__name',
          'lugar__name',
          'estado__name',
          'descripcion',
          'evidencia_encode',
          'accion_plan',
          'evidencia_correctiva_encode',
          'date',
          'programacion_general_id__contratista__name',
          'programacion_general_id__transporte__name',
          'programacion_general_id__conductor_placa__placa1',
          'programacion_general_id__conductor_placa__placa2'
          )
    elif contratista_id != -1 and lugar_id != -1:
      observaciones = Observaciones.objects.filter(
        date__range = [data['start_date'],data['end_date']],
        programacion_general_id__contratista__id = contratista_id,
        lugar_id = lugar_id
        ).values(
          'id',
          'categoria__name',
          'lugar__name',
          'estado__name',
          'descripcion',
          'evidencia_encode',
          'accion_plan',
          'evidencia_correctiva_encode',
          'date',
          'programacion_general_id__contratista__name',
          'programacion_general_id__transporte__name',
          'programacion_general_id__conductor_placa__placa1',
          'programacion_general_id__conductor_placa__placa2'
          )
    elif contratista_id != -1 and categoria_id != -1:
      observaciones = Observaciones.objects.filter(
        date__range = [data['start_date'],data['end_date']],
        programacion_general_id__contratista__id = contratista_id,
        categoria_id = categoria_id
        ).values(
          'id',
          'categoria__name',
          'lugar__name',
          'estado__name',
          'descripcion',
          'evidencia_encode',
          'accion_plan',
          'evidencia_correctiva_encode',
          'date',
          'programacion_general_id__contratista__name',
          'programacion_general_id__transporte__name',
          'programacion_general_id__conductor_placa__placa1',
          'programacion_general_id__conductor_placa__placa2'
          )
    elif lugar_id != -1 and categoria_id != -1:
      observaciones = Observaciones.objects.filter(
        date__range = [data['start_date'],data['end_date']],
        lugar_id = lugar_id,
        categoria_id = categoria_id
        ).values(
          'id',
          'categoria__name',
          'lugar__name',
          'estado__name',
          'descripcion',
          'evidencia_encode',
          'accion_plan',
          'evidencia_correctiva_encode',
          'date',
          'programacion_general_id__contratista__name',
          'programacion_general_id__transporte__name',
          'programacion_general_id__conductor_placa__placa1',
          'programacion_general_id__conductor_placa__placa2'
          )
    elif contratista_id != -1:
      observaciones = Observaciones.objects.filter(
        date__range = [data['start_date'],data['end_date']],
        programacion_general_id__contratista__id = contratista_id      
        ).values(
          'id',
          'categoria__name',
          'lugar__name',
          'estado__name',
          'descripcion',
          'evidencia_encode',
          'accion_plan',
          'evidencia_correctiva_encode',
          'date',
          'programacion_general_id__contratista__name',
          'programacion_general_id__transporte__name',
          'programacion_general_id__conductor_placa__placa1',
          'programacion_general_id__conductor_placa__placa2'
          )
    elif lugar_id != -1:
      observaciones = Observaciones.objects.filter(
        date__range = [data['start_date'],data['end_date']],
        lugar_id = lugar_id      
        ).values(
          'id',
          'categoria__name',
          'lugar__name',
          'estado__name',
          'descripcion',
          'evidencia_encode',
          'accion_plan',
          'evidencia_correctiva_encode',
          'date',
          'programacion_general_id__contratista__name',
          'programacion_general_id__transporte__name',
          'programacion_general_id__conductor_placa__placa1',
          'programacion_general_id__conductor_placa__placa2'
          )
    elif categoria_id != -1:
      observaciones = Observaciones.objects.filter(
        date__range = [data['start_date'],data['end_date']],
        categoria_id = categoria_id      
        ).values(
          'id',
          'categoria__name',
          'lugar__name',
          'estado__name',
          'descripcion',
          'evidencia_encode',
          'accion_plan',
          'evidencia_correctiva_encode',
          'date',
          'programacion_general_id__contratista__name',
          'programacion_general_id__transporte__name',
          'programacion_general_id__conductor_placa__placa1',
          'programacion_general_id__conductor_placa__placa2'
          )
    else:
      observaciones = Observaciones.objects.filter(
        date__range = [data['start_date'],data['end_date']]
        ).values(
          'id',
          'categoria__name',
          'lugar__name',
          'estado__name',
          'descripcion',
          'evidencia_encode',
          'accion_plan',
          'evidencia_correctiva_encode',
          'date',
          'programacion_general_id__contratista__name',
          'programacion_general_id__transporte__name',
          'programacion_general_id__conductor_placa__placa1',
          'programacion_general_id__conductor_placa__placa2'
          )
    
    request.session['start_date'] = data['start_date']
    request.session['end_date'] = data['end_date']

    if not observaciones:
      return JsonResponse({"resultado": "vacio"})

    fo = []
    
    for obs in observaciones:
      fo = FotosObservaciones.objects.filter(observacion_id = obs['id'])
      if fo:
        aux = []        
        for f in fo:
          my_dict = {"id":f.id, "id_obs": f.observacion_id, "evidencia_encode": f.evidencia_encode, "evidencia_correctiva_encode": f.evidencia_correctiva_encode}
          aux.append(my_dict)
        obs.update({"fotos": aux})
      
    json = list(observaciones)    
    return JsonResponse({"resultado": json})

def generate_pdf(request):  
  if not request.user.is_authenticated or request.user.role.id >= 4:
    return redirect("/")
  start_date = request.session.get('start_date')
  end_date = request.session.get('end_date')

  observaciones = Observaciones.objects.filter(date__range = [start_date, end_date])
  fotos = []
  contador = 0
  for obs in observaciones:
      fotos.append(FotosObservaciones.objects.filter(observacion_id = obs.id))

  template_path = 'r_pdf.html'
  context = {'observaciones': observaciones,'fotos': fotos, 'STATIC_ROOT': settings.STATIC_ROOT, 'start_date': start_date, 'end_date': end_date}
  # context = {'myvar': 'this is your template context'}
  # Create a Django response object, and specify content_type as pdf
  response = HttpResponse(content_type='application/pdf')
  # if download
  # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
  # if display
  response['Content-Disposition'] = 'filename="report.pdf"'
  # find the template and render it.
  template = get_template(template_path)
  html = template.render(context)

  # create a pdf
  pisa_status = pisa.CreatePDF(
      html, dest=response)
  # if error then show some funy view
  if pisa_status.err:
      return HttpResponse('We had some errors <pre>' + html + '</pre>')
  return response

from io import BytesIO 
import xlsxwriter
from PIL import Image
import base64

def generate_excel(request):
    # create our spreadsheet.  I will create it in memory with a StringIO
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    start_date = request.session.get('start_date')
    end_date = request.session.get('end_date')
    observaciones = Observaciones.objects.filter(date__range =[start_date, end_date])  
            
    #tamaño de celda que coincida con 0.5 de la imagen
    cell_width = 45.0
    cell_height = 180.0
    #aumentar tamaño de celda para las imagenes 
    worksheet.set_column(1, 12, cell_width/2)
    worksheet.set_column(8, 8, cell_width)
    worksheet.set_column(12, 12, cell_width)
    worksheet.set_default_row(cell_height)
    worksheet.set_row(0, 40)
    x_scale = 0.5
    y_scale = 0.5
    
    #info cabecera
    format = workbook.add_format()
    format.set_font_size(18)
    format.set_bold(True)   
    format.set_text_wrap() 
    format.set_fg_color('#9b7c69')
    format.set_font_color('white')
    worksheet.write('A1', "ITEM", format)
    worksheet.write('B1', "FECHA", format)
    worksheet.write('C1', "LUGAR", format)
    worksheet.write('D1', "CONTRATISTA", format)
    worksheet.write('E1', "EMPRESA TRANSPORTISTA", format)
    worksheet.write('F1', "UNIDAD INVOLUCRADA", format)
    worksheet.write('G1', "CATEGORÍA DE EVENTO", format)
    worksheet.write('H1', "DESCRIPCIÓN", format)
    worksheet.write('I1', "EVIDENCIA FOTOGRÁFICA", format)
    worksheet.write('J1', "PLAN DE ACCIÓN", format)
    worksheet.write('K1', "RESPONSABLE", format)
    worksheet.write('L1', "FECHA DE LEVANTAMIENTO", format)
    worksheet.write('M1', "EVIDENCIA CORRECTIVA", format)
    i = 1
    undefined = "PENDIENTE"
    #alinear centro
    format2 = workbook.add_format()
    format2.set_valign('center')
    format2.set_valign('vcenter')       
    format2.set_text_wrap() 
    for obs in observaciones:      
      worksheet.write('A'+ str(i +1), i, format2)
      worksheet.write('B'+ str(i +1), obs.date, format2)
      worksheet.write('C'+ str(i +1), obs.lugar.name, format2)
      worksheet.write('D'+ str(i +1), obs.programacion_general_id.contratista.name, format2)
      worksheet.write('E'+ str(i +1), obs.programacion_general_id.conductor_placa.placa1 + '|' + obs.programacion_general_id.conductor_placa.placa2, format2)
      worksheet.write('F'+ str(i +1), obs.programacion_general_id.transporte.name, format2)
      worksheet.write('G'+ str(i +1), obs.categoria.name, format2)
      worksheet.write('H'+ str(i +1), obs.descripcion, format2)
      if obs.evidencia_encode != "undefined":
        data = obs.evidencia_encode[2:-1]
        imgdata = base64.b64decode(data)
        image = BytesIO(imgdata)
        worksheet.insert_image('I'+ str(i +1), 'myimage.png', {'image_data': image, 'x_scale': x_scale, 'y_scale': y_scale})
        #insertar mas fotoes evidencia si tiene
        fo = (FotosObservaciones.objects.filter(observacion_id = obs.id))
        if fo:          
          worksheet.set_row(i, cell_height * (len(fo) + 1))
          aux_contador = 1
          for f in fo:
            if f.evidencia_encode and f.evidencia_encode != "undefined":
              data = f.evidencia_encode[2:-1]
              imgdata = base64.b64decode(data)
              image = BytesIO(imgdata)
              worksheet.insert_image('I'+ str(i +1), 'foto_evidencia.png', {'image_data': image, 'x_scale': x_scale, 'y_scale': y_scale, 'y_offset': (cell_height * aux_contador) + (60 * aux_contador) })
              print(cell_height * aux_contador)
              aux_contador = aux_contador +1 
      else:
        worksheet.write('I'+ str(i +1), undefined, format2)
      worksheet.write('J'+ str(i +1), obs.accion_plan, format2)
      worksheet.write('K'+ str(i +1), "CONTRATISTA", format2)
      worksheet.write('L'+ str(i +1), obs.date, format2)
      if obs.evidencia_correctiva_encode != "undefined":
        data = obs.evidencia_correctiva_encode[2:-1]
        imgdata = base64.b64decode(data)
        image = BytesIO(imgdata)
        worksheet.insert_image('M'+ str(i +1), 'myimage.png', {'image_data': image, 'x_scale': x_scale, 'y_scale': y_scale})    
        #insertar mas fotoes evidencia ocrrectiva si tiene
        fo = (FotosObservaciones.objects.filter(observacion_id = obs.id))
        if fo:
          aux_contador = 1
          for f in fo:
            if f.evidencia_correctiva_encode and f.evidencia_correctiva_encode != "undefined":
              data = f.evidencia_correctiva_encode[2:-1]
              imgdata = base64.b64decode(data)
              image = BytesIO(imgdata)
              worksheet.insert_image('M'+ str(i +1), 'foto_correctiva.png', {'image_data': image, 'x_scale': x_scale, 'y_scale': y_scale, 'y_offset':  (cell_height * aux_contador) + (60 * aux_contador) })
              aux_contador = aux_contador +1 
      else:
        worksheet.write('M'+ str(i +1), undefined, format2)    
      i = i +1
    workbook.close()

    # create a response
    response = HttpResponse(content_type='application/vnd.ms-excel')

    # tell the browser what the file is named
    response['Content-Disposition'] = 'attachment;filename="repote '+start_date+'-'+end_date+'.xlsx"'

    # put the spreadsheet data into the response
    response.write(output.getvalue())

    # return the response
    return response