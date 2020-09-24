from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from rest_framework import generics,serializers
from rest_framework.pagination import CursorPagination

from .decorators import unauthenticated_user
from .forms import CreateUserForm
from .models import Message


@login_required(login_url='login/')
def index(request):
    template = 'chat/chatroom.html'
    #messages = Message.objects.all().order_by('timestamp')
    return render(request, template)


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.username')
    class Meta:
        model = Message
        fields = ['text', 'timestamp','sender']


class MessagePagination(CursorPagination):
    page_size= 10
    page_size_query_param = 'page_size'
    ordering = '-timestamp'


class MessagesListView(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    pagination_class = MessagePagination


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
