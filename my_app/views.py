from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import User

# Create your views here.


def index(request):
    if not request.user.is_authenticated:
        return render(request, "login.html", {"message": "please login"})
    else:
        return render(request, "index.html")


def login_view(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "login.html", {"error": "username or password error"})


def logout_view(request):
    logout(request)
    return render(request, "login.html", {"message": "logout success"})


def register_view(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        tipo = request.POST.get("tipo")
        ci = request.POST.get("ci")
        telefono = request.POST.get("telefono")
        password = request.POST.get("password")
        password_again = request.POST.get("password_again")

        if password != password_again:
            return render(request, "register.html", {"error": "password not match"})

        new_user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            tipo=tipo,
            ci=ci,
            telefono=telefono,
        )
        new_user.save()
        return render(
            request, "login.html", {"message": "Account created successfully"}
        )
    else:
        return render(request, "register.html")

