from django.shortcuts import render, redirect

from UsuariosApp.forms import UserForm  
from UsuariosApp.models import User, Role, UserType
from TrabajadoresApp.models import Worker

from django.http import JsonResponse, HttpResponse

from django.contrib.auth.hashers import make_password

def create(request):  
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/") 
    roles = Role.objects.all()  
    if request.method == "POST":  
        form = UserForm(request.POST)        
        
        datos = request.POST
        password=make_password(datos['password'])
        dni=datos['dni']
        username=datos['username']
        role_id=datos['role'] 
        
        if form.is_valid():  
            try:                
                User(dni=dni, username=username, password=password, role_id = role_id).save()  
                UserType(dni=dni, username=username, password=password, role_id = role_id).save()  
                if int(role_id) == 4:
                    Worker(dni=dni, username=username, slept_hours = 0, area_id=1).save()  
                return redirect('/users/index')  
            except:  
                pass  
    else:  
        form = UserForm()  
       
    return render(request,'u_new.html',{'form':form, 'roles':roles}) 

def index(request):     
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/") 
    users = User.objects.all()  
    return render(request,"u_index.html",{'users':users})  

def show(request, id):  
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/") 
    users = User.objects.get(id=id)  
    return render(request,"u_show.html",{'user':users}) 

def edit(request, id):  
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/") 
    users = User.objects.get(id=id)  
    roles = Role.objects.all()  
    return render(request,'u_edit.html', {'user':users, 'roles':roles})  

def update(request, id):  
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/") 
    if request.method == "POST":  
        users = User.objects.get(id=id) 
        datos = request.POST
        password=users.password
        dni=datos['dni']
        username=datos['username']
        role_id=datos['role'] 

        if 3 > 1:  
            User.objects.filter(id=id).update(dni=dni, username=username, password=password, role_id = role_id)
            UserType.objects.filter(dni=dni).update(dni=dni, username=username, password=password, role_id = role_id)
            if int(role_id) == 4:
                    Worker.objects.filter(dni=dni).update(dni=dni, username=username, slept_hours = 0, area_id=1)
            return redirect("/users/index")  
    return render(request, 'u_edit.html', {'users': users})  

def destroy(request, id):  
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/") 
    users = User.objects.get(id=id)  
    users.delete()  
    UserType.objects.filter(dni=users.dni).delete()
    Worker.objects.filter(dni=users.dni).delete() 
    return redirect("/users/index")  

def edit_password(request, id):  
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/") 
    users = User.objects.get(id=id)  
    roles = Role.objects.all()  
    return render(request,'up_edit.html', {'user':users, 'roles':roles})  

def update_password(request, id):  
    if not request.user.is_authenticated or request.user.role.id >= 4:
        return redirect("/") 
    if request.method == "POST":  
        users = User.objects.get(id=id) 
        datos = request.POST
        password=make_password(datos['password'])
        dni=datos['dni']
        username=datos['username']
        role_id=datos['role'] 

        if 3 > 1:  
            User.objects.filter(id=id).update(dni=dni, username=username, password=password, role_id = role_id)
            UserType.objects.filter(dni=dni).update(dni=dni, username=username, password=password, role_id = role_id)
            if int(role_id) == 4:
                    Worker.objects.filter(dni=dni).update(dni=dni, username=username, slept_hours = 0, area_id=1)
            return redirect("/users/index")  
    return render(request, 'up_edit.html', {'users': users})  
