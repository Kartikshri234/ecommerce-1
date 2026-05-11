"""Authentication Views - Registration, Login, Logout"""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from shop.forms import RegisterForm


def register_view(request):
    """Handle user registration"""
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! 🎉")
            return redirect(request.GET.get("next") or "home")
        messages.error(request, "Please fix the errors below and try again.")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    """Handle user login"""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back {user.username}!")
            return redirect(request.GET.get("next") or "home")
        else:
            messages.error(request, "Invalid username or password ❌")
    return render(request, "login.html")


def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("home")
