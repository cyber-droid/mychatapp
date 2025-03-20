from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('room', room_name='testroom')
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