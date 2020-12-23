from django.shortcuts import render, redirect

from EmpresasApp.forms import CompanyForm  
from EmpresasApp.models import Company  
# Create your views here.  
def create(request):  
    if not request.user.is_authenticated or request.user.role.id >= 3:
        return redirect("/") 
    if request.method == "POST":  
        form = CompanyForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('/companies/index')  
            except:  
                pass  
    else:  
        form = CompanyForm()  
    return render(request,'c_new.html',{'form':form}) 

def index(request):  
    if not request.user.is_authenticated or request.user.role.id >= 3:
        return redirect("/") 
    companies = Company.objects.all()  
    return render(request,"c_index.html",{'companies':companies})  

def show(request, id):  
    if not request.user.is_authenticated or request.user.role.id >= 3:
        return redirect("/") 
    companies = Company.objects.get(id=id)  
    return render(request,"c_show.html",{'company':companies}) 

def edit(request, id):  
    if not request.user.is_authenticated or request.user.role.id >= 3:
        return redirect("/") 
    companies = Company.objects.get(id=id)  
    return render(request,'c_edit.html', {'company':companies})  

def update(request, id):  
    if not request.user.is_authenticated or request.user.role.id >= 3:
        return redirect("/") 
    companies = Company.objects.get(id=id)  
    form = CompanyForm(request.POST, instance = companies)  
    if form.is_valid():  
        form.save()  
        return redirect("/companies/index")  
    return render(request, 'a_edit.html', {'companies': companies})  

def destroy(request, id):  
    if not request.user.is_authenticated or request.user.role.id >= 3:
        return redirect("/") 
    companies = Company.objects.get(id=id)  
    companies.delete()  
    return redirect("/companies/index")  
