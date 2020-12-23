from django.shortcuts import render, redirect

from FatigasApp.forms import FatigueForm  
from FatigasApp.models import Fatigue  
from TrabajadoresApp.models import Worker 
# Create your views here.  
def create(request):  
    if not request.user.is_authenticated or request.user.role.id >= 3:
        return redirect("/") 
    if request.method == "POST":  
        form = FatigueForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('/fatigues/index')  
            except:  
                pass  
    else:  
        form = FatigueForm()  
        workers = Worker.objects.all()  
    return render(request,'f_new.html',{'form':form, 'workers':workers}) 

def index(request):  
    if not request.user.is_authenticated or request.user.role.id >= 3:
        return redirect("/") 
    fatigues = Fatigue.objects.all()  
    return render(request,"f_index.html",{'fatigues':fatigues})  

def show(request, id):  
    if not request.user.is_authenticated or request.user.role.id >= 3:
        return redirect("/") 
    fatigues = Fatigue.objects.get(id=id)  
    return render(request,"f_show.html",{'fatigue':fatigues}) 

def edit(request, id):  
    if not request.user.is_authenticated or request.user.role.id >= 3:
        return redirect("/") 
    fatigues = Fatigue.objects.get(id=id)  
    workers = Worker.objects.all()  
    return render(request,'f_edit.html', {'fatigue':fatigues, 'workers':workers})  

def update(request, id):  
    if not request.user.is_authenticated or request.user.role.id >= 3:
        return redirect("/") 
    fatigues = Fatigue.objects.get(id=id)  
    form = FatigueForm(request.POST, instance = fatigues)  
    if form.is_valid():  
        form.save()  
        return redirect("/fatigues/index")  
    return render(request, 'f_edit.html', {'fatigues': fatigues})  

def destroy(request, id):  
    if not request.user.is_authenticated or request.user.role.id >= 3:
        return redirect("/") 
    fatigues = Fatigue.objects.get(id=id)  
    fatigues.delete()  
    return redirect("/fatigues/index")  
