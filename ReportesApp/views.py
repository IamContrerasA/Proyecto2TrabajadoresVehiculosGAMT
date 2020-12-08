from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from ExcelApp.models import Observaciones, Lugar, Contratista, Categoria
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa

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

    if contratista_id != -1:
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
    json = list(observaciones)    
    return JsonResponse({"resultado": json})

def generate_pdf(request):  
  if not request.user.is_authenticated or request.user.role.id >= 4:
    return redirect("/")
  start_date = request.session.get('start_date')
  end_date = request.session.get('end_date')

  observaciones = Observaciones.objects.filter(date__range = [start_date, end_date])

  template_path = 'r_pdf.html'
  context = {'observaciones': observaciones, 'STATIC_ROOT': settings.STATIC_ROOT, 'start_date': start_date, 'end_date': end_date}
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