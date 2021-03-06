from calendar import month
from django import db
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from datetime import timedelta, date


import calendar

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return date(year, month, day)


class Paquete(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    precio = models.FloatField()
    foto = models.ImageField(upload_to='paquetes', null=True, blank=True)
    qr = models.ImageField(upload_to='qrs', null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "paquetes"

    def __str__(self):
        return f"<Paquete: {self.nombre}>"


class User(AbstractUser):
    ci = models.IntegerField(unique=True)
    telefono = models.IntegerField(null=True)
    tipo = models.CharField(max_length=20, null=False, blank=False)
    foto = models.ImageField(upload_to='users', null=True, blank=True)
    suscrito = models.BooleanField(default=False)
    parqueado = models.BooleanField(default=False)
    class Meta:
        db_table = "users"

    def __str__(self) -> str:
        return f"<User: {self.username}>"


class CompraPaquete(models.Model):
    paquete = models.ForeignKey(Paquete, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    tipo_pago = models.CharField(max_length=50)
    activo = models.BooleanField(default=False)
    pendiente = models.BooleanField(default=True) # nuevo
    comprobante = models.ImageField(upload_to='comprobantes', null=True, blank=True)

    class Meta:
        db_table = "compra_paquetes"

    def fecha_literal(self):
        meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        return f"{self.fecha_compra.day} de {meses[self.fecha_compra.month - 1]} de {self.fecha_compra.year}"

    def dias_restantes(self):
        if self.activo:
            """
            dia = self.fecha_compra.day
            mes = self.fecha_compra.month
            year = self.fecha_compra.year
            fecha_actual = datetime.now()
            fecha_inicio = datetime(year, mes, dia) + timedelta(month=1)
            result = fecha_inicio - datetime.now()
            return result.days
            """
            dia = self.fecha_compra.day
            mes = self.fecha_compra.month
            year = self.fecha_compra.year

            fecha_actual = date.today()
            fecha_inicio = datetime(year, mes, dia)
            fecha_fin = add_months(fecha_inicio, 1)
            
            result = fecha_fin - fecha_actual
            return result.days
        else:
            return timedelta(days=0)

class TipoVehiculo(models.Model):
    nombre = models.CharField(max_length=30)

    class Meta:
        db_table = "tipo_vehiculos"

    def __str__(self) -> str:
        return f"<TipoVehiculo: {self.nombre}>"


class Vehiculo(models.Model):

    placa = models.CharField(max_length=20, null=False)
    modelo = models.CharField(max_length=20, null=False)
    color = models.CharField(max_length=20, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.ForeignKey(TipoVehiculo, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='vehiculos', null=True, blank=True)
    class Meta:
        db_table = "vehiculos"

    def __str__(self):
        return f"<Vehiculo: {self.placa} - {self.modelo}>"


class Parqueo(models.Model):

    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(default=datetime.now())
    activo = models.BooleanField(default=True)
    class Meta:
        db_table = "parqueos"

    def __str__(self):
        return f"<Parqueo: {self.nombre}>"


class DetalleParqueo(models.Model):
    __tablename__ = "detalle_parqueos"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parqueo = models.ForeignKey(Parqueo, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    fecha_entrada = models.DateTimeField(default=datetime.now())
    fecha_salida = models.DateTimeField(null=True)

    class Meta:
        db_table = "detalle_parqueos"

    def __str__(self):
        return f"<DetalleParqueo: {self.user} - {self.parqueo} - {self.vehiculo} - {self.fecha_entrada} - {self.fecha_salida}>"
