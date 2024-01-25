from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm, RegistrationForm, DigitalWillForm
from .models import User
import json
import bcrypt  # Import the bcrypt library

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            entered_password = form.cleaned_data['password']
            
            try:
                with open('users.json', 'r') as file:
                    users = json.load(file)
            except FileNotFoundError:
                users = []

            for user in users:
                if user['username'] == username:
                    # Decode the stored hashed password from string to bytes
                    stored_hashed_password = user['password'].encode('utf-8')

                    # Check the entered password against the stored hashed password
                    if bcrypt.checkpw(entered_password.encode('utf-8'), stored_hashed_password):
                        return home_view(request)

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

            try:
                with open('users.json', 'r') as file:
                    users = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                users = []

            # Hash the password using bcrypt
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Convert the bytes to a string before saving it in the user data
            user_data = {'username': username, 'password': hashed_password.decode('utf-8'), 'balance': 0.0}
            users.append(user_data)

            with open('users.json', 'w') as file:
                json.dump(users, file, indent=2)

            return redirect('login') 
    else:
        form = RegistrationForm()

    return render(request, 'masquaradeApp/register.html', {'form': form, 'error': ''})



def landing_page(request):
    return render(request, 'masquaradeApp/landing.html')

def home_view(request):
    with open('users.json') as json_file:
        user_data = json.load(json_file)

    if request.method == 'POST':
        entered_username = request.POST.get('username')
        entered_password = request.POST.get('password')

        for user in user_data:
            if user['username'] == entered_username:
                # Decode the stored hashed password from string to bytes
                stored_hashed_password = user['password'].encode('utf-8')

                # Check the entered password against the stored hashed password
                if bcrypt.checkpw(entered_password.encode('utf-8'), stored_hashed_password):
                    return render(request, 'masquaradeApp/home.html', {'balance': user['balance']})

    return render(request, 'masquaradeApp/home.html')

def read_user_data(file_path):
    try:
        with open(file_path, 'r') as file:
            users_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        users_data = []
    return users_data

def write_user_data(file_path, users_data):
    with open(file_path, 'w') as file:
        json.dump(users_data, file, indent=2)

def digital_will_view(request):
    file_path = 'users.json'

    request_data = {
        'method': request.method,
        'user': request.user.username if request.user.is_authenticated else None,
        'POST': dict(request.POST),
    }

    if request.method == 'POST':
        form = DigitalWillForm(request.POST)
        if form.is_valid():
            recipient_username = form.cleaned_data['recipient']
            amount = float(form.cleaned_data['amount'])
            password = form.cleaned_data['password']

            users_data = read_user_data(file_path)

            sender = next((user for user in users_data if user['username'] == request.user.username), None)
            recipient = next((user for user in users_data if user['username'] == recipient_username), None)

            if sender is None or recipient is None:
                return render(request, 'masquaradeApp/digital_will.html')

            if sender['password'] != password:
                return render(request, 'masquaradeApp/digital_will.html', {'form': form, 'error': 'Incorrect password'})

            if sender['balance'] >= amount:
                sender['balance'] -= amount
                recipient['balance'] += amount

                print(amount)
                write_user_data(file_path, users_data)

                return redirect('home')
            else:
                print(f'Error: Insufficient balance. User: {request.user.username}, Amount: {amount}')
                return render(request, 'masquaradeApp/digital_will.html', {'form': form, 'error': 'Insufficient balance'})

    else:
        form = DigitalWillForm()

    return render(request, 'masquaradeApp/digital_will.html', {'form': form, 'error': ''})