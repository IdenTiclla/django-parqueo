from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

# Create your views here.


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html', {'message': 'please login'})
    else:
        return render(request, 'index.html')

def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, 'login.html', {'error': 'username or password error'})

def logout_view(request):
    logout(request)
    return render(request, 'login.html', {'message': 'logout success'})

def register(request):
    return render(request, 'register.html')