from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import User, AuthenticationForm
from django.contrib import messages
from .forms import LoginForm
#from .models import Parents, Children


def login_view(request):
    if request.method == 'POST':
        
        name = request.POST.get('name', '').strip()
        birth_year = request.POST.get('birth_year', '').strip()
        password = request.POST.get('password', '').strip()

        user = None
        if name and birth_year:
            user = authenticate(request, username=name, password=birth_year)
        if not user and name and password:
            user = authenticate(request, username=name, password=password)

        if user:
            login(request, user)
            display_name = user.username 
            person = Parents.objects.filter(user=user).first()
            if not person:
                person = Children.objects.filter(user=user).first()
            
            if person:
                display_name = person.name


            messages.success(request, f"Welcome back, {display_name}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid Credentials.")
            
    return render(request, 'auth/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')