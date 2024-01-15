from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm, RegistrationForm, DigitalWillForm
from .models import User
import json

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            try:
                with open('users.json', 'r') as file:
                    users = json.load(file)
            except FileNotFoundError:
                users = []

            for user in users:
                if user['username'] == username and user['password'] == password:
                    return home_view(request)
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

            try:
                with open('users.json', 'r') as file:
                    users = json.load(file)
                    if not isinstance(users, list):
                        print(f"Unexpected data format in users.json: {users}")
                        users = []
            except FileNotFoundError:
                users = []

            user_data = {'username': username, 'password': password, 'balance': 0.0}
            users.append(user_data)

            with open('users.json', 'w') as file:
                json.dump(users, file)

            return redirect('login') 
    else:
        form = RegistrationForm()

    return render(request, 'masquaradeApp/register.html', {'form': form, 'error': ''}) 
def landing_page(request):
    return render(request, 'masquaradeApp/landing.html')

import json
from django.shortcuts import render

def home_view(request):
    # Load user data from users.json
    with open('users.json') as json_file:
        user_data = json.load(json_file)

    if request.method == 'POST':
        # Assuming the form has 'username' and 'password' fields
        entered_username = request.POST.get('username')
        entered_password = request.POST.get('password')

        # Check if entered username and password match any user in the user_data
        for user in user_data:
            if user['username'] == entered_username and user['password'] == entered_password:
                # If the credentials are correct, return the user's balance
                return render(request, 'masquaradeApp/home.html', {'balance': user['balance']})
    
    # If the credentials are incorrect or the request method is not POST, render the home template without balance
    return render(request, 'masquaradeApp/home.html')

def read_user_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return []

def write_user_data(file_path, users_data):
    with open(file_path, 'w') as file:
        json.dump(users_data, file, indent=2)

def digital_will_view(request):
    file_path = 'users.json'  # Replace with the actual path to your 'users.json' file

    if request.method == 'POST':
        form = DigitalWillForm(request.POST)
        if form.is_valid():
            recipient_username = form.cleaned_data['recipient']
            amount = float(form.cleaned_data['amount'])
            password = form.cleaned_data['password']

            # Read user data from the JSON file
            users_data = read_user_data(file_path)

            # Find the sender and recipient
            sender = next((user for user in users_data if user['username'] == request.user.username), None)
            recipient = next((user for user in users_data if user['username'] == recipient_username), None)

            # Check if sender and recipient exist
            if sender is None or recipient is None:
                return render(request, 'masquaradeApp/digital_will.html', {'form': form, 'error': 'Invalid sender or recipient'})

            # Check if the password is correct
            if sender['password'] != password:
                return render(request, 'masquaradeApp/digital_will.html', {'form': form, 'error': 'Incorrect password'})

            # Check if the user has enough balance
            if sender['balance'] >= amount:
                # Deduct the amount from the sender's balance
                sender['balance'] -= amount

                # Update or create an entry for the recipient
                recipient['balance'] += amount

                # Save the modified user data back to the JSON file
                write_user_data(file_path, users_data)

                # Redirect to the home page with the updated balance
                return redirect('home')
            else:
                print(f'Error: Insufficient balance. User: {request.user.username}, Amount: {amount}')
                return render(request, 'masquaradeApp/digital_will.html', {'form': form, 'error': 'Insufficient balance'})

    else:
        form = DigitalWillForm()

    return render(request, 'masquaradeApp/digital_will.html', {'form': form, 'error': ''})
