from datetime import datetime
from functools import total_ordering
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import DetalleParqueo, Paquete, User, TipoVehiculo, Vehiculo, CompraPaquete, Parqueo

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
    if  not paquetes:
        messages.warning(request, "Registra almenos un paquete para continuar")
        return redirect("crear_paquete")
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
    if not vehiculos:
        messages.warning(request, "No tienes vehiculos registrados Registra almenos un vehiculo para continuar")
        return redirect("registrar_vehiculo")
    return render(request, "mis_vehiculos.html", {"vehiculos": vehiculos})

def comprar_paquetes_view(request):
    user = request.user
    if not user.suscrito:
        paquetes = Paquete.objects.all()
        return render(request, "comprar_paquetes.html", {"paquetes": paquetes})
    else:
        messages.warning(request, "Ya estas suscrito")
        return redirect("mis_suscripciones")
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

def mis_suscripciones_view(request):
    compras = CompraPaquete.objects.filter(user=request.user)
    if not compras:
        messages.warning(request, "No tienes suscripciones registradas compra almenos una suscripcion para continuar")
        return redirect("comprar_paquetes")
    return render(request, "mis_suscripciones.html", {"compras": compras})

def activaciones_view(request):
    compras = CompraPaquete.objects.filter(activo=False)
    return render(request, "activaciones.html", {"compras": compras})

def activar_view(request, id):
    if request.method == "POST":
        compra_paquete = CompraPaquete.objects.get(id=id)
        compra_paquete.activo = True
        compra_paquete.user.suscrito = True
        compra_paquete.user.save()
        compra_paquete.save()
        
        messages.success(request, "Activacion realizada exitosamente!")
        return render(request, "activaciones.html")

def crear_parqueo_view(request):
    if request.method == "GET":
        return render(request, "crear_parqueo.html")
    elif request.method == "POST":
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        
        new_parqueo = Parqueo(nombre=nombre, descripcion=descripcion)
        new_parqueo.save()
        
        messages.success(request, "Parqueo creado exitosamente!")
        return render(request, "crear_parqueo.html")

def mis_parqueos_view(request):
    parqueos = Parqueo.objects.all()
    if  not parqueos:
        messages.warning(request, "Registra almenos un parqueo para continuar")
        return redirect("crear_parqueo")
    return render(request, "mis_parqueos.html", {"parqueos": parqueos})

def parqueo_view(request):
    user = request.user
    # si no tenemos suscripciones, no podemos ver los parqueos
    if not user.suscrito:
        messages.error(request, "No tienes suscripcion")
        return redirect("comprar_paquetes")
    # si el usuario no tiene vehiculos registrados
    vehiculos = user.vehiculo_set.all()
    if not vehiculos:
        messages.warning(request, "Registra almenos un vehiculo para continuar")
        return redirect("registrar_vehiculo")
    
    if user.parqueado:
        detalle_parqueo = DetalleParqueo.objects.filter(user=user, fecha_salida=None).first()
        enlace = f"https://django-parqueo.herokuapp.com/marcar_salida/{detalle_parqueo.id}"
        
        return render(request, "parqueo.html", {"detalle_parqueo": detalle_parqueo, "enlace": enlace})


    parqueos = Parqueo.objects.all()
    return render(request, "parqueo.html", {"parqueos": parqueos})

def parquear_view(request, id):
    parqueo = Parqueo.objects.get(id=id)
    user = request.user
    vehiculos = user.vehiculo_set.all()
    if request.method == "GET":
        return render(request, "parquear.html", {"parqueo": parqueo, "vehiculos": vehiculos})
    elif request.method == "POST":
        id_vehiculo = request.POST.get("vehiculo_id")
        vehiculo = Vehiculo.objects.get(id=id_vehiculo)
        
        detalle_parqueo = DetalleParqueo(user=user, parqueo=parqueo, vehiculo=vehiculo)
        detalle_parqueo.save()
        parqueo.activo = False
        parqueo.save()
        user.parqueado = True
        user.save()
        messages.success(request, "Parqueado exitosamente!")
        
        return render(request, "parqueo.html")

def marcar_salidas_view(request):
    detalle_parqueos = DetalleParqueo.objects.filter(fecha_salida=None)
    return render(request, "marcar_salidas.html", {"detalle_parqueos": detalle_parqueos})


def marcar_salida_view(request, id):
    if request.method == "GET":
        detalle_parqueo = DetalleParqueo.objects.get(id=id)
        detalle_parqueo.fecha_salida = datetime.now()
        detalle_parqueo.parqueo.activo = True
        detalle_parqueo.parqueo.save()
        detalle_parqueo.user.parqueado = False
        detalle_parqueo.user.save()
        detalle_parqueo.save()
        messages.success(request, "Salida registrada exitosamente!")
        return redirect("marcar_salidas")

def ver_salidas_view(request):
    if request.method == "GET":
        return render(request, "ver_salidas.html")
    elif request.method == "POST":
        fecha_salida = request.POST.get("fecha_salida")
        fecha_salida = datetime.strptime(fecha_salida, "%Y-%m-%d")
        
        dia = fecha_salida.day
        year = fecha_salida.year
        mes = fecha_salida.month

        detalle_parqueos = DetalleParqueo.objects.filter(fecha_salida__day=f'{dia}', fecha_salida__year=f'{year}', fecha_salida__month=f'{mes}')
        return render(request, "ver_salidas.html", {"detalle_parqueos": detalle_parqueos})
        return redirect("ver_salidas")



def reportes_suscripciones_compradas_view(request):
    if request.method == "GET":
        return render(request, "reportes_suscripciones_compradas.html")
    elif request.method == "POST":
        fecha_inicio = request.POST.get("fecha_inicio")
        fecha_fin = request.POST.get("fecha_fin")
        fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
        compras = CompraPaquete.objects.filter(fecha_compra__range=(fecha_inicio, fecha_fin))
        total = 0
        for compra in compras:
            total += compra.paquete.precio
        return render(request, "reportes_suscripciones_compradas.html", {"compras": compras, "total": total})