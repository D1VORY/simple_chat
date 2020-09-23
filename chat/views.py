from django.shortcuts import render
from .models import Message
# Create your views here.



def index(request):
    template = 'chat/chatroom.html'
    messages = reversed(Message.objects.all().order_by('-timestamp'))
    return render(request, template, context = {'messages':messages})
