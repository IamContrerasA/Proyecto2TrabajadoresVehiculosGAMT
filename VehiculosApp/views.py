from django.shortcuts import render, redirect

from VehiculosApp.forms import VehicleForm  
from VehiculosApp.models import Vehicle  
# Create your views here.  
def create(request):  
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/") 
    if request.method == "POST":  
        form = VehicleForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('/vehicles/index')  
            except:  
                pass  
    else:  
        form = VehicleForm()  
    return render(request,'v_new.html',{'form':form}) 

def index(request):  
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/") 
    vehicles = Vehicle.objects.all()  
    return render(request,"v_index.html",{'vehicles':vehicles})  

def show(request, id):  
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/") 
    vehicles = Vehicle.objects.get(id=id)  
    return render(request,"v_show.html",{'vehicle':vehicles}) 

def edit(request, id):  
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/") 
    vehicles = Vehicle.objects.get(id=id)  
    return render(request,'v_edit.html', {'vehicle':vehicles})  

def update(request, id):  
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/") 
    vehicles = Vehicle.objects.get(id=id)  
    form = VehicleForm(request.POST, instance = vehicles)  
    if form.is_valid():  
        form.save()  
        return redirect("/vehicles/index")  
    return render(request, 'v_edit.html', {'vehicles': vehicles})  

def destroy(request, id):  
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/") 
    vehicles = Vehicle.objects.get(id=id)  
    vehicles.delete()  
    return redirect("/vehicles/index")  
