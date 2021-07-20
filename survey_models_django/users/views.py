from django.http import request
from django.shortcuts import redirect, render
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout


def register(request):
    form = CreateUserForm()
    error = None
    if request.method == 'POST':
        print(request.POST)
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        else:
            error = "Invalid data, check the fields"

    context = {'form':form, 'error':error}
    return render(request, 'users/register.html', context)

def login_user(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('tests_list')
    context = {}
    return render(request, 'users/login.html', context)

def logout_user(request):
    logout(request)
    return redirect('login')