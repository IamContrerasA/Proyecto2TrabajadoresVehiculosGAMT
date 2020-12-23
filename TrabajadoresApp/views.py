from django.shortcuts import render, redirect

from TrabajadoresApp.forms import WorkerForm
from TrabajadoresApp.models import Worker
from AreasApp.models import Area
from VehiculosApp.models import Vehicle
from EmpresasApp.models import Company
from FatigasApp.models import Fatigue
from FatigasApp.forms import FatigueForm
from CheckListApp.models import CheckList
from CheckListApp.forms import CheckListForm

from django.http import JsonResponse, HttpResponse

from django.contrib.auth.decorators import login_required

def emp(request):
    if not request.user.is_authenticated or request.user.role.id >= 3:
        return redirect("/") 
    if request.method == "POST":
        form = WorkerForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/workers/index')
            except:
                pass
    else:
        form = WorkerForm()
        areas = Area.objects.all()
    return render(request, 'new.html', {'form': form, 'areas': areas})

def index(request):
    if not request.user.is_authenticated or request.user.role.id >= 3:
        return redirect("/") 
    workers = Worker.objects.all()
    return render(request, "index.html", {'workers': workers})


def show(request, id):
    if not request.user.is_authenticated or request.user.role.id >= 3:
        return redirect("/") 
    workers = Worker.objects.get(id=id)
    return render(request, "show.html", {'worker': workers})


def edit(request, id):
    if not request.user.is_authenticated or request.user.role.id >= 3:
        return redirect("/") 
    workers = Worker.objects.get(id=id)
    areas = Area.objects.all()
    return render(request, 'edit.html', {'worker': workers, 'areas': areas})


def update(request, id):
    if not request.user.is_authenticated or request.user.role.id >= 3:
        return redirect("/") 
    workers = Worker.objects.get(id=id)
    form = WorkerForm(request.POST, instance=workers)
    if form.is_valid():
        form.save()
        return redirect("/workers/index")
    return render(request, 'edit.html', {'workers': workers})


def destroy(request, id):
    if not request.user.is_authenticated or request.user.role.id >= 3:
        return redirect("/") 
    workers = Worker.objects.get(id=id)
    workers.delete()
    return redirect("/workers/index")



def r_create(request, id):    
    if not request.user.is_authenticated or request.user.role.id >= 3:
        return redirect("/") 
    if request.method == "POST":
        form = FatigueForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/workers/'+str(id)+'/results/index')
            except:
                pass
    else:
        form = FatigueForm()  
        worker = Worker.objects.get(id=id)
        fatigue = Fatigue.objects.filter(worker_id=id)              
    return render(request, 'results/r_new.html', {'form': form, 'worker': worker, 'fatigue': fatigue})

def r_index(request, id):
    if not request.user.is_authenticated or request.user.role.id >= 3:
        return redirect("/") 
    worker = Worker.objects.get(id=id)
    fatigues = Fatigue.objects.filter(worker_id=id).order_by('time_to_wake')
    json_fatigues = list(fatigues.values())

    if request.method == 'POST':         
        return JsonResponse({"json_fatigues": json_fatigues})

    return render(request, "results/r_index.html", {'worker': worker, 'fatigues': fatigues})

def r_show(request, id, id2):
    if not request.user.is_authenticated or request.user.role.id >= 3:
        return redirect("/") 
    fatigue = Fatigue.objects.get(id=id2)
    return render(request, "results/r_show.html", {'fatigue': fatigue})


def r_edit(request, id, id2):
    if not request.user.is_authenticated or request.user.role.id >= 3:
        return redirect("/") 
    fatigue = Fatigue.objects.get(id=id2)
    return render(request, 'results/r_edit.html', {'fatigue': fatigue})


def r_update(request, id, id2):
    if not request.user.is_authenticated or request.user.role.id >= 3:
        return redirect("/") 
    fatigue = Fatigue.objects.get(id=id2)
    form = FatigueForm(request.POST, instance=fatigue)
    if form.is_valid():
        form.save()
        return redirect('/workers/'+str(id)+'/results/index')
    return render(request, 'results/r_edit.html', {'workers': workers})


def r_destroy(request, id, id2):
    if not request.user.is_authenticated or request.user.role.id >= 3:
        return redirect("/") 
    fatigue = Fatigue.objects.get(id=id2)
    fatigue.delete()
    return redirect('/workers/'+str(id)+'/results/index')

def wr_create(request):    
    if not request.user.is_authenticated:
        return redirect("/") 
    
    if request.method == "POST":
        form = FatigueForm(request.POST)        
        if form.is_valid():
            try:
                form.save()
                return redirect('/workers/result_hours/index')
            except:
                pass
    else:
        form = FatigueForm()  
        worker = Worker.objects.get(dni=request.user.dni)
        fatigue = Fatigue.objects.filter(worker_id=worker.id)              
    return render(request, 'only_workers/wr_new.html', {'form': form, 'worker': worker, 'fatigue': fatigue})

def wr_index(request):
    if not request.user.is_authenticated:
        return redirect("/") 
    
    worker = Worker.objects.get(dni = request.user.dni)
    fatigues = Fatigue.objects.filter(worker_id=worker.id).order_by('time_to_wake')
    json_fatigues = list(fatigues.values())
    
    if request.method == 'POST':                 
        return JsonResponse({"json_fatigues": json_fatigues})

    return render(request, "only_workers/wr_index.html", {'worker': worker, 'fatigues': fatigues})

def wcl_create(request):    
    if not request.user.is_authenticated:
        return redirect("/") 
    
    if request.method == "POST":  
        indice = request.POST
        id=indice['worker']     
        CheckList.objects.filter(worker_id=id).filter(current = True).update(current = False)
                
        form = CheckListForm(request.POST) 
                
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
    return render(request,'only_workers/wcl_new.html',{'form':form, 'workers':workers, 'vehicles':vehicles, 'companies':companies}) 