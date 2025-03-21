from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import logging

# Set up logging
logger = logging.getLogger(__name__)

def register(request):
    if request.method == 'POST':
        try:
            form = UserCreationForm(request.POST)
            if form.is_valid():
                logger.info("Form is valid, saving user...")
                user = form.save()
                logger.info(f"User {user.username} saved successfully.")
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                logger.info(f"Authenticating user {username}...")
                user = authenticate(username=username, password=password)
                if user is not None:
                    logger.info(f"User {username} authenticated successfully.")
                    login(request, user)
                    logger.info(f"User {username} logged in successfully.")
                    return redirect('room', room_name='testroom')
                else:
                    logger.error(f"Authentication failed for user {username}.")
                    return render(request, 'chat/register.html', {'form': form, 'error': 'Authentication failed.'})
            else:
                logger.warning("Form is invalid.")
                return render(request, 'chat/register.html', {'form': form})
        except Exception as e:
            logger.error(f"Error during registration: {str(e)}", exc_info=True)
            return render(request, 'chat/register.html', {'form': form, 'error': f'Registration failed: {str(e)}'})
    else:
        form = UserCreationForm()
    return render(request, 'chat/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('room', room_name='testroom')
        else:
            return render(request, 'chat/login.html', {'error': 'Invalid username or password'})
    return render(request, 'chat/login.html')

@login_required
def room(request, room_name):
    return render(request, 'chat/room.html', {'room_name': room_name})