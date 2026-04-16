from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import ensure_csrf_cookie
from .forms import LoginForm


@ensure_csrf_cookie
def login_view(request):
    """
    Handle user login. Supports authentication via:
    - Username and password
    """
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = LoginForm()  # Initialize form for GET requests

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name", "").strip()
            password = form.cleaned_data.get("password", "").strip()

            # Try to authenticate with username and password
            user = authenticate(request, username=name, password=password)

            if user:
                login(request, user)
                display_name = user.get_full_name() or user.username
                messages.success(request, f"Welcome back, {display_name}!")
                return redirect("dashboard")
            else:
                form.add_error(
                    None, "Invalid credentials. Please check your name and password."
                )

    return render(request, "auth/login.html", {"form": form})


def logout_view(request):
    """Log out the current user and redirect to login page."""
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("login")
