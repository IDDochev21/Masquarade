from django.shortcuts import render, redirect
from .forms import LoginForm, RegistrationForm
from .models import User
import json

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Check if user exists in JSON file (you may want to use a database in a real scenario)
            try:
                with open('users.json', 'r') as file:
                    users = json.load(file)
            except FileNotFoundError:
                users = []

            for user in users:
                if user['username'] == username and user['password'] == password:
                    return redirect('success')  # Redirect to a success page
            else:
                return render(request, 'masquaradeApp/login.html', {'form': form, 'error': 'Invalid credentials'})

    else:
        form = LoginForm()

    return render(request, 'masquaradeApp/login.html', {'form': form, 'error': ''})


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if password != confirm_password:
                return render(request, 'masquaradeApp/register.html', {'form': form, 'error': 'Passwords do not match'})

            # Save user information to the JSON file (you may want to use a database in a real scenario)
            try:
                with open('users.json', 'r') as file:
                    users = json.load(file)
            except FileNotFoundError:
                users = []

            users.append({'username': username, 'password': password})

            with open('users.json', 'w') as file:
                json.dump(users, file)

            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = RegistrationForm()

    return render(request, 'masquaradeApp/register.html', {'form': form, 'error': ''})

def landing_page(request):
    return render(request, 'masquaradeApp/landing.html')