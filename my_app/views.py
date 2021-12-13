from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Paquete, User, TipoVehiculo, Vehiculo, CompraPaquete

# Create your views here.


def index(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Inicia sesion para continuar")
        return render(request, "login.html")
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
        messages.error(request, "Usuario o contraseña incorrectos")
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    messages.warning(request, "Inicia sesion para continuar")
    return render(request, "login.html")


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
        foto = request.FILES['foto']

        if password != password_again:
            messages.error(request, "Las contraseñas no coinciden")
            return render(request, "register.html")

        new_user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            tipo=tipo,
            ci=ci,
            telefono=telefono,
            foto=foto
        )
        if tipo == "Administrador":
            new_user.is_superuser = True
            new_user.is_staff = True
        new_user.save()
        messages.success(request, "Usuario registrado")
        return render(request, "login.html")
    else:
        return render(request, "register.html")

def perfil_view(request):
    return render(request, "perfil.html")

def crear_paquete_view(request):
    if request.method == "GET":
        return render(request, "crear_paquete.html")
    else:
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        precio = request.POST.get("precio")
        qr = request.FILES['qr']
        foto = request.FILES['foto']

        paquete = Paquete(nombre=nombre, descripcion=descripcion, precio=precio, qr=qr, foto=foto)
        paquete.save()
        messages.success(request, "Paquete creado exitosamente!")
        return render(request, "crear_paquete.html")

def paquetes_view(request):
    paquetes = Paquete.objects.all()
    return render(request, "paquetes.html", {"paquetes": paquetes})
    
def registrar_vehiculo_view(request):
    if request.method == "GET":
        tipos = TipoVehiculo.objects.all()
        return render(request, "registrar_vehiculo.html", {"tipos": tipos})
    else:
        placa = request.POST.get("placa")
        modelo = request.POST.get("modelo")
        color = request.POST.get("color")
        user = request.user
        foto = request.FILES['foto']
        tipo_id = request.POST.get("tipo")
        tipo = TipoVehiculo.objects.get(id=tipo_id)

        new_vehiculo = Vehiculo.objects.create(placa=placa, modelo=modelo, color=color, user=user, tipo=tipo, foto=foto)
        new_vehiculo.save()
        messages.success(request, "Vehiculo registrado exitosamente!")
        return render(request, "registrar_vehiculo.html")

def mis_vehiculos_view(request):
    vehiculos = request.user.vehiculo_set.all()
    return render(request, "mis_vehiculos.html", {"vehiculos": vehiculos})

def comprar_paquetes_view(request):
    paquetes = Paquete.objects.all()
    return render(request, "comprar_paquetes.html", {"paquetes": paquetes})

def comprar_view(request, id):
    paquete = Paquete.objects.get(id=id)
    if request.method == "GET":
        return render(request, "comprar_paquete.html", {"paquete": paquete})
    elif request.method == "POST":
        user = request.user
        compra_paquete = CompraPaquete(user=user, paquete=paquete)
        compra_paquete.tipo_pago = "Deposito"
        compra_paquete.activo = False
        compra_paquete.comprobante = request.FILES['comprobante']

        compra_paquete.save()
        messages.success(request, "Compra realizada exitosamente!")
        return render(request, "comprar_paquetes.html")
