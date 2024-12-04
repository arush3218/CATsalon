from django.shortcuts import render
from .models import Room, Topic
from .forms import RoomForm, Room
from django.shortcuts import redirect


# rooms = [
#     {'id': '1', 'name': 'Lets learn something'},
#     {'id': '2', 'name': 'Dont learn something'},
#     {'id': '3', 'name': 'Might learn something'},
# ]

def home(request):
    q= request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(topic__name__icontains=q)
    topics = Topic.objects.all()
    context = {'rooms': rooms, 'topics': topics}
    return render(request, 'base/home.html',context )

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
        
    return render(request, 'base/room.html', context)

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
