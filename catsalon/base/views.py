from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Topic
from .forms import RoomForm, Room
from django.db.models import Q
from django.contrib.auth.models import User 
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# rooms = [
#     {'id': '1', 'name': 'Lets learn something'},
#     {'id': '2', 'name': 'Dont learn something'},
#     {'id': '3', 'name': 'Might learn something'},
# ]


def loginPage(request):
    
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('home')
       
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'User does not exist')
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'Username or password incorrect')
            
            
    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
        page = 'register'
        
        if request.user.is_authenticated:
            return redirect('home')
        
        form = UserCreationForm()
        
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('home')
            
        context = {'form': form, 'page': page}
        return render(request, 'base/login_register.html',context)
    
def home(request):
    q= request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q)| 
                                Q(name__icontains=q) |
                                Q(description__icontains=q)
                                )
    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}
    return render(request, 'base/home.html',context )

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
        
    return render(request, 'base/room.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/form.html',context)

def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    
    if request.user != room.host :
        return HttpResponse('You are not allowed here!')
        
    
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
       
    context = {'form': form}
    return render(request, 'base/form.html', context)

def DeleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        redirect('home')
    return render(request, 'base/delete.html',{'obj':room})



'''
user1 ===== Felis_catus password= justacat
user2 ===== arush password= bellacia0
user3 ===== siamese password= justacat

'''