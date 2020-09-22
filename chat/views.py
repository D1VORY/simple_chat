from django.shortcuts import render

# Create your views here.



def index(request):
    template = 'chat/chatroom.html'

    return render(request, template)
