from django.shortcuts import render, redirect

from AreasApp.forms import AreaForm  
from AreasApp.models import Area  
# Create your views here.  
def create(request): 
    if not request.user.is_authenticated or request.user.role.id >= 3:
        return redirect("/") 
    if request.method == "POST":  
        form = AreaForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('/areas/index')  
            except:  
                pass  
    else:  
        form = AreaForm()  
    return render(request,'a_new.html',{'form':form}) 

def index(request):  
    if not request.user.is_authenticated or request.user.role.id >= 3:
        return redirect("/")
    areas = Area.objects.all()  
    return render(request,"a_index.html",{'areas':areas})  

def show(request, id):
    if not request.user.is_authenticated or request.user.role.id >= 3:
        return redirect("/")  
    areas = Area.objects.get(id=id)  
    return render(request,"a_show.html",{'area':areas}) 

def edit(request, id):  
    if not request.user.is_authenticated or request.user.role.id >= 3:
        return redirect("/")
    areas = Area.objects.get(id=id)  
    return render(request,'a_edit.html', {'area':areas})  

def update(request, id): 
    if not request.user.is_authenticated or request.user.role.id >= 3:
        return redirect("/") 
    areas = Area.objects.get(id=id)  
    form = AreaForm(request.POST, instance = areas)  
    if form.is_valid():  
        form.save()  
        return redirect("/areas/index")  
    return render(request, 'a_edit.html', {'areas': areas})  

def destroy(request, id):  
    if not request.user.is_authenticated or request.user.role.id >= 3:
        return redirect("/")
    areas = Area.objects.get(id=id)  
    areas.delete()  
    return redirect("/areas/index")  
