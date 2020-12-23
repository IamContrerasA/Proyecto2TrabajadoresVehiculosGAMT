from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from UsuariosApp.forms import UserCreateForm

def base(request):
    if not request.user.is_authenticated or request.user.role.id >= 3:
        return redirect("/") 
    return render(request, 'base.html')

@login_required
def welcome(request):
    if request.user.role.id >= 4:
        return render(request, 'welcome_workers.html')

    return render(request, 'welcome.html')


def save_index(request):
    if not request.user.is_authenticated or request.user.role.id >= 3:
        return redirect("/") 
    return render(request, 'save_index.html')


def signup(request, *args, **kwargs):
    if not request.user.is_authenticated or request.user.role.id >= 3:
        return redirect("/") 
    if request.method == "POST":
        form = UserCreateForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = UserCreateForm()

    return render(request, 'registration/signup.html', {
        'form': form
    })
