from django.shortcuts import render, redirect

from CheckListApp.forms import CheckListForm  
from CheckListApp.models import CheckList  
from TrabajadoresApp.models import Worker
from VehiculosApp.models import Vehicle
from EmpresasApp.models import Company

from django.http import JsonResponse, HttpResponse

def create(request):  
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/") 
    if request.method == "POST":  
        indice = request.POST
        id=indice['worker']
        #cambiar el valor actual de true a false para luego crear el nuevo registro
        CheckList.objects.filter(worker_id=id).filter(current = True).update(current = False)
        #RETORNA LA LISTA DE TODOS
        #worker = CheckList.objects.filter(worker_id=id).order_by('-current')
        #json_fatigues = list(worker.values())
        #return JsonResponse({"a": json_fatigues})
        #print(worker)
        
        form = CheckListForm(request.POST) 
        
        #Tratar de asignar el campo current a true desde el view
        #return HttpResponse({Worker.objects.get(id=indice['worker'])})
        #return HttpResponse({form['worker']})
        #return HttpResponse({form})
        if form.is_valid():  
            try:                
                form.save()  
                return redirect('/check_lists/index')  
            except:  
                pass  
    else:  
        form = CheckListForm()  
        workers = Worker.objects.all()  
        vehicles = Vehicle.objects.all()  
        companies = Company.objects.all()  
    return render(request,'cl_new.html',{'form':form, 'workers':workers, 'vehicles':vehicles, 'companies':companies}) 

def index(request):  
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/") 
    check_lists = CheckList.objects.all()  
    return render(request,"cl_index.html",{'check_lists':check_lists})  

def show(request, id):  
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/") 
    check_lists = CheckList.objects.get(id=id)  
    return render(request,"cl_show.html",{'check_list':check_lists}) 

def edit(request, id):  
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/") 
    check_lists = CheckList.objects.get(id=id)  
    workers = Worker.objects.all()  
    vehicles = Vehicle.objects.all() 
    return render(request,'cl_edit.html', {'check_list':check_lists, 'workers':workers, 'vehicles':vehicles})  

def update(request, id):  
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/") 
    check_lists = CheckList.objects.get(id=id)  
    form = CheckListForm(request.POST, instance = check_lists)  
    if form.is_valid():  
        form.save()  
        return redirect("/check_lists/index")  
    return render(request, 'cl_edit.html', {'check_lists': check_lists})  

def destroy(request, id):  
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/") 
    check_lists = CheckList.objects.get(id=id)  
    check_lists.delete()  
    return redirect("/check_lists/index")  