from django.shortcuts import render, redirect
from .models import Message

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .decorators import unauthenticated_user
from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required

@login_required(login_url='login/')
def index(request):
    template = 'chat/chatroom.html'
    messages = reversed(Message.objects.all().order_by('-timestamp'))
    return render(request, template, context = {'messages':messages})


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account was created for {username}')
            return redirect('login')

    context = {'form':form}
    return render(request, 'chat/register.html', context)


@unauthenticated_user
def loginPage(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username , password = password)

        if user is not None :
            login(request,user)
            return redirect('index')
        else:
            messages.info(request, 'username or password is incorrect')
            return render(request, 'chat/login.html', context)

    return render(request, 'chat/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')
