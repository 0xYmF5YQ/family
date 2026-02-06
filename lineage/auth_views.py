from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import User, AuthenticationForm
from django.contrib import messages



def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, "auth/signup.html", {
                "username": username,
                "email": email
            })

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, "auth/signup.html", {
                "email": email
            })

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already in use.")
            return render(request, "auth/signup.html", {
                "username": username
            })
        User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        messages.success(request, "Account created successfully! Please log in.")
        return render(request, "auth/signup.html")
    return render(request, "auth/signup.html")

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('dashboard')

            messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    else:
        form = AuthenticationForm()

    return render(request, 'auth/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')