import email
import imp
from pydoc_data.topics import topics
from unicodedata import name
from django.shortcuts import render

from myapp.forms import MyUserCreationForm, RoomForm, UserForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.db.models import Q
from . models import  User, Room, Topic, Message

# Create your views here.

def loginUserPage(request):
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')
    
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')
    context = {'page': page}
    return render(request, 'user/login_register.html', context)
    

def registerUserPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            # user.is_superuser = True
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
    return render(request, 'user/login_register.html', {'form': form})


def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def homePage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__contains=q) |
        Q(name__contains=q) |
        Q(description__contains=q)
    )
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile', pk=user.id)
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__contains=q))[0:3]
    context = {'rooms': rooms, 'topics':topics, 'room_count': room_count, 'room_messages': room_messages}
    context['form'] = form
    return render(request, 'main/home.html', context)


@login_required(login_url='login')
def userProfile(request, pk):
    user = user.objects.get(id=pk)
    rooms = user.room_set.all()
    messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {
        'user': user,
        'rooms': rooms,
        'messages': messages,
        'topic': topics
    }
    return render(request, 'user/profile.html', context)


@login_required(login_url='login')
def topicPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'main/topic_componet.html', {'topics': topics})


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_id = request.POST.get('topic')
        # topic_name = Topic.objects.filter(id=topic_id, many=False)
        # print(f"topic {topic_name[0].name}")
        topic, created = Topic.objects.get_or_create(id=topic_id)

        Room.objects.create(
            user = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
        return redirect('home')
    
    context = {'form': form, 'topics': topics}
    return render(request, 'room/create_room.html', context)