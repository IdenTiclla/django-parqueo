from django import db
from django.db import models
from django.contrib.auth.models import AbstractUser





class Paquete(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    precio = models.FloatField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'paquetes'

    def __str__(self):
        return f'<Paquete: {self.nombre}>'

class User(AbstractUser):
    genero = models.BooleanField(default=True)
    tipo = models.CharField(max_length=20, null=False, blank=False)

    class Meta:
        db_table = 'users'

    def __str__(self) -> str:
        return f"<User: {self.username}>"

class CompraPaquete(models.Model):
    fecha_compra = models.DateTimeField(auto_now_add=True)
    paquete = models.ForeignKey(Paquete, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo_pago = models.CharField(max_length=50)

    class Meta:
        db_table = 'compra_paquetes'

class TipoVehiculo(models.Model):
    nombre = models.CharField(max_length=30)

    class Meta:
        db_table = 'tipo_vehiculos'
    
    def __str__(self) -> str:
        return f"<TipoVehiculo: {self.nombre}>"

class Vehiculo(models.Model):
    
    placa = models.CharField(max_length=20, null=False)
    model = models.CharField(max_length=20, null=False)
    color = models.CharField(max_length=20, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.ForeignKey(TipoVehiculo, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'vehiculos'
    
    def __str__(self):
        return f'<Vehiculo: {self.placa} - {self.year}>'

    
class Parqueo(models.Model):
    
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'parqueos'
    
    def __str__(self):
        return f'<Parqueo: {self.nombre}>'

class DetalleParqueo(models.Model):
    __tablename__ = 'detalle_parqueos'
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parqueo = models.ForeignKey(Parqueo, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    fecha_entrada = models.DateTimeField(auto_now_add=True)
    fecha_salida = models.DateTimeField(null=True)

    class Meta:
        db_table = 'detalle_parqueos'

    def __str__(self):
        return f'<DetalleParqueo: {self.user} - {self.parqueo} - {self.vehicle}>'
    
